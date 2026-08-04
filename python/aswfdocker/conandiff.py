# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tracks and merges vendored Conan recipes against their upstream
Conan Center Index (CCI) source, using a single JSON manifest
(packages/conan/recipes/conan-center-index-upstream.json) instead of
per-file "# From: ..." header comments.
"""

import base64
import dataclasses
import difflib
import json
import logging
import os
import subprocess
import tempfile
import typing

import click
import yaml
from github import Auth, Github
from github.GithubException import GithubException

from aswfdocker import constants, index, settings

logger = logging.getLogger(__name__)

UPSTREAM_JSON_NAME = "conan-center-index-upstream.json"


# ---------------------------------------------------------------------------
# JSON manifest I/O
# ---------------------------------------------------------------------------


def upstream_json_path(repo_root: str) -> str:
    return os.path.join(repo_root, "packages", "conan", "recipes", UPSTREAM_JSON_NAME)


def load_upstream_data(repo_root: str) -> dict:
    path = upstream_json_path(repo_root)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_upstream_data(repo_root: str, data: dict) -> None:
    path = upstream_json_path(repo_root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def iter_folder_shas(entry: dict) -> typing.Iterator[typing.Tuple[str, str]]:
    """Normalizes a manifest entry (single- or multi-version) into (folder, sha) pairs."""
    if entry.get("class") != "cci":
        return
    if "versions" in entry:
        for folder, info in entry["versions"].items():
            yield folder, info["sha"]
    else:
        yield entry["folder"], entry["sha"]


def local_path_for(repo_root: str, recipe_name: str, entry: dict, folder: str) -> str:
    """Maps a manifest (recipe, folder) unit to its on-disk directory.

    Single-version recipes are flattened to the recipe root locally, even when
    their upstream folder isn't literally "all" (e.g. b2 -> portable). Multi-
    version recipes (qt/onetbb) preserve the upstream version-folder name
    locally.
    """
    recipe_dir = os.path.join(repo_root, "packages", "conan", "recipes", recipe_name)
    if "versions" in entry:
        return os.path.join(recipe_dir, folder)
    return recipe_dir


# ---------------------------------------------------------------------------
# Scope resolution (--group / --target, mirrors build's semantics)
# ---------------------------------------------------------------------------


def _resolve_recipe_names(
    groups: typing.Sequence[str], targets: typing.Sequence[str]
) -> typing.List[str]:
    idx = index.Index()
    package_groups = idx.groups[constants.ImageType.PACKAGE]
    groups = list(groups)
    targets = list(targets)
    if not groups and targets:
        groups = sorted(
            {idx.get_group_from_image(constants.ImageType.PACKAGE, t) for t in targets}
        )
    if not groups and not targets:
        return sorted({name for names in package_groups.values() for name in names})
    names = []
    for g in groups:
        if g not in package_groups:
            raise click.BadOptionUsage("--group", f"Group {g} is not valid!")
        names.extend(package_groups[g])
    if targets:
        names = [n for n in names if n in targets]
    return names


# ---------------------------------------------------------------------------
# GitHub access
# ---------------------------------------------------------------------------


class CCIGitHub:
    """Wraps access to conan-io/conan-center-index (mirrors releaser.GitHub).

    Scopes and caches network access for the lifetime of the instance: tree
    listings are fetched per-recipe-folder (never the whole monorepo tree),
    and repeated lookups of the same ref/blob within one `--merge` run are
    served from cache instead of re-fetched. This matters against GitHub's
    unauthenticated rate limit (60 req/hour) once more than a couple of
    recipes are in scope.
    """

    def __init__(self):
        s = settings.Settings()
        if s.github_access_token:
            auth = Auth.Token(s.github_access_token)
            self.github = Github(auth=auth)
        else:
            self.github = Github()
        self.repo = self.github.get_repo(
            f"{constants.CCI_GITHUB_ORG}/{constants.CCI_GITHUB_REPO_NAME}"
        )
        self._commit_sha_cache: typing.Dict[str, str] = {}
        self._blob_cache: typing.Dict[str, bytes] = {}

    def get_ref_sha(self, ref: str) -> str:
        if ref not in self._commit_sha_cache:
            sha = self.repo.get_commit(ref).sha
            self._commit_sha_cache[ref] = sha
            self._commit_sha_cache[sha] = sha  # alias so re-resolving a sha is free
        return self._commit_sha_cache[ref]

    def get_folder_commits(self, path: str, ref: str):
        """Returns PyGithub's lazily-paginated commit list for `path`.

        Callers must iterate this directly (as `check_recipe` does, breaking
        as soon as it finds the tracked SHA) rather than materializing it with
        `list()`/`len()` — doing so forces a walk of the folder's *entire*
        commit history (every commit that ever touched any file under it),
        which for a widely-touched package can be dozens of pages/API calls
        for a single recipe.
        """
        return self.repo.get_commits(path=path, sha=ref)

    def get_latest_folder_commit(self, path: str, ref: str):
        """Returns just the newest commit touching `path`, or None — fetches
        only the first page of history, not the whole thing."""
        for commit in self.repo.get_commits(path=path, sha=ref):
            return commit
        return None

    def get_commit_for_sha(self, path: str, sha: str):
        for commit in self.repo.get_commits(path=path, sha=sha):
            return commit
        return None

    def get_config_yml_versions(self, upstream_name: str, ref: str):
        try:
            content_file = self.repo.get_contents(
                f"recipes/{upstream_name}/config.yml", ref=ref
            )
        except GithubException as e:
            if e.status == 404:
                return None
            raise
        content = base64.b64decode(content_file.content)
        return yaml.safe_load(content)

    def folder_exists(self, upstream_name: str, folder: str, ref: str) -> bool:
        try:
            self.repo.get_contents(f"recipes/{upstream_name}/{folder}", ref=ref)
            return True
        except GithubException as e:
            if e.status == 404:
                return False
            raise

    def get_tree_at_ref(self, path: str, ref: str) -> typing.Dict[str, str]:
        """Recursively lists files under `path` at `ref`.

        Scoped to `path` only: lists that folder's immediate contents (one
        call), then does one recursive `git/trees` call per immediate
        subdirectory found (scoped to that subdirectory's own tree sha, e.g.
        `test_package/`). This never walks or fetches the rest of the CCI
        monorepo's tree, unlike listing from the commit's root tree.
        """
        result: typing.Dict[str, str] = {}
        try:
            entries = self.repo.get_contents(path, ref=ref)
        except GithubException as e:
            if e.status == 404:
                return result
            raise
        if not isinstance(entries, list):
            entries = [entries]
        for item in entries:
            if item.type == "dir":
                subtree = self.repo.get_git_tree(item.sha, recursive=True)
                for sub_entry in subtree.tree:
                    if sub_entry.type == "blob":
                        result[f"{item.name}/{sub_entry.path}"] = sub_entry.sha
            else:
                result[item.name] = item.sha
        return result

    def get_blob_content(self, blob_sha: str) -> bytes:
        if blob_sha not in self._blob_cache:
            blob = self.repo.get_git_blob(blob_sha)
            self._blob_cache[blob_sha] = base64.b64decode(blob.content)
        return self._blob_cache[blob_sha]


# ---------------------------------------------------------------------------
# Report mode
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class OutdatedFolder:
    recipe: str
    folder: str
    tracked_sha: str
    newer_commits: list


@dataclasses.dataclass
class RemovedFolder:
    recipe: str
    folder: str
    reason: str


@dataclasses.dataclass
class ConanDiffError:
    recipe: str
    folder: str
    message: str


@dataclasses.dataclass
class ConanDiffReport:
    outdated: list = dataclasses.field(default_factory=list)
    removed: list = dataclasses.field(default_factory=list)
    errors: list = dataclasses.field(default_factory=list)


def check_recipe(
    gh: CCIGitHub, recipe_name: str, entry: dict, branch: str
) -> typing.Tuple[list, list]:
    outdated = []
    errors = []
    upstream_name = entry.get("upstream_name", recipe_name)
    for folder, sha in iter_folder_shas(entry):
        path = f"recipes/{upstream_name}/{folder}"
        try:
            tracked_commit = gh.get_commit_for_sha(path, sha)
        except GithubException as e:
            errors.append(ConanDiffError(recipe_name, folder, str(e)))
            continue
        if tracked_commit is None:
            errors.append(
                ConanDiffError(
                    recipe_name, folder, f"tracked sha {sha} not found for {path}"
                )
            )
            continue
        all_commits = gh.get_folder_commits(path, branch)
        newer = []
        for commit in all_commits:
            if commit.sha == tracked_commit.sha:
                break
            newer.append(commit)
        if newer:
            outdated.append(OutdatedFolder(recipe_name, folder, sha, newer))
    return outdated, errors


def check_removed_versions(
    gh: CCIGitHub, recipe_name: str, entry: dict, branch: str
) -> list:
    if "versions" not in entry:
        return []
    upstream_name = entry.get("upstream_name", recipe_name)
    removed = []
    config = gh.get_config_yml_versions(upstream_name, branch)
    tracked_folders = set(entry["versions"].keys())
    if config is None:
        return [
            RemovedFolder(recipe_name, folder, "config.yml missing upstream")
            for folder in tracked_folders
        ]
    referenced = set()
    for info in (config.get("versions") or {}).values():
        if isinstance(info, dict) and "folder" in info:
            referenced.add(info["folder"])
    for folder in tracked_folders:
        if folder not in referenced:
            removed.append(
                RemovedFolder(recipe_name, folder, "no longer referenced in config.yml")
            )
    return removed


def run_conandiff(
    repo_root: str,
    groups: typing.Sequence[str] = (),
    targets: typing.Sequence[str] = (),
    branch: str = constants.CCI_DEFAULT_BRANCH,
) -> ConanDiffReport:
    names = _resolve_recipe_names(groups, targets)
    data = load_upstream_data(repo_root)
    recipes = data.get("recipes", {})
    report = ConanDiffReport()
    gh = None
    for name in sorted(names):
        entry = recipes.get(name)
        if entry is None or entry.get("class") != "cci":
            continue
        if gh is None:
            gh = CCIGitHub()
        outdated, errors = check_recipe(gh, name, entry, branch)
        report.outdated.extend(outdated)
        report.errors.extend(errors)
        report.removed.extend(check_removed_versions(gh, name, entry, branch))
    return report


# ---------------------------------------------------------------------------
# --merge: real 3-way merge via git merge-file
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class MergeConflict:
    recipe: str
    path: str
    reason: str


@dataclasses.dataclass
class RecipeMergeResult:
    recipe: str
    added: list = dataclasses.field(default_factory=list)
    removed: list = dataclasses.field(default_factory=list)
    merged: list = dataclasses.field(default_factory=list)
    conflicts: list = dataclasses.field(default_factory=list)
    skipped_reason: str = ""

    @property
    def clean(self) -> bool:
        return not self.conflicts and not self.skipped_reason


@dataclasses.dataclass
class ConanMergeReport:
    results: list = dataclasses.field(default_factory=list)

    def clean_recipes(self) -> typing.Set[str]:
        return {r.recipe for r in self.results if r.clean}


def _is_binary(content: bytes) -> bool:
    return b"\0" in content


def _git_status_porcelain(repo_root: str, path: str) -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", path],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _list_local_files(local_path: str) -> typing.Set[str]:
    result: typing.Set[str] = set()
    if not os.path.isdir(local_path):
        return result
    for root, _, files in os.walk(local_path):
        for fname in files:
            fpath = os.path.join(root, fname)
            result.add(os.path.relpath(fpath, local_path))
    return result


def _three_way_merge_file(
    local_file: str, base_content: bytes, theirs_content: bytes
) -> bool:
    """Merges upstream changes into local_file in place via `git merge-file`.

    Returns True if conflict markers were left in the file.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = os.path.join(tmpdir, "base")
        theirs_path = os.path.join(tmpdir, "theirs")
        with open(base_path, "wb") as f:
            f.write(base_content)
        with open(theirs_path, "wb") as f:
            f.write(theirs_content)
        result = subprocess.run(
            [
                "git",
                "merge-file",
                "-L",
                "ours",
                "-L",
                "base",
                "-L",
                "theirs",
                "--diff3",
                local_file,
                base_path,
                theirs_path,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode != 0


def _merge_recipe(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    repo_root: str,
    gh: CCIGitHub,
    recipe_name: str,
    entry: dict,
    branch: str,
    force: bool,
) -> RecipeMergeResult:
    recipe_dir = os.path.join(repo_root, "packages", "conan", "recipes", recipe_name)
    result = RecipeMergeResult(recipe=recipe_name)
    if not force:
        status = _git_status_porcelain(repo_root, recipe_dir)
        if status:
            result.skipped_reason = (
                f"uncommitted changes in {recipe_dir}, use --force to override"
            )
            return result

    upstream_name = entry.get("upstream_name", recipe_name)
    new_ref_sha = gh.get_ref_sha(branch)
    for folder, sha in iter_folder_shas(entry):
        local_path = local_path_for(repo_root, recipe_name, entry, folder)
        upstream_path = f"recipes/{upstream_name}/{folder}"
        base_tree = gh.get_tree_at_ref(upstream_path, sha)
        theirs_tree = gh.get_tree_at_ref(upstream_path, new_ref_sha)
        local_files = _list_local_files(local_path)
        for relpath in sorted(set(base_tree) | set(theirs_tree) | local_files):
            local_file = os.path.join(local_path, relpath)
            in_base = relpath in base_tree
            in_theirs = relpath in theirs_tree
            in_local = relpath in local_files

            if not in_base and in_theirs:
                theirs_content = gh.get_blob_content(theirs_tree[relpath])
                if in_local:
                    with open(local_file, "rb") as f:
                        local_content = f.read()
                    if local_content != theirs_content:
                        result.conflicts.append(
                            MergeConflict(
                                recipe_name,
                                relpath,
                                "added upstream but a differing local file already exists",
                            )
                        )
                        continue
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                with open(local_file, "wb") as f:
                    f.write(theirs_content)
                result.added.append(relpath)

            elif in_base and not in_theirs:
                if not in_local:
                    continue
                base_content = gh.get_blob_content(base_tree[relpath])
                with open(local_file, "rb") as f:
                    local_content = f.read()
                if local_content == base_content:
                    os.remove(local_file)
                    result.removed.append(relpath)
                else:
                    result.conflicts.append(
                        MergeConflict(
                            recipe_name,
                            relpath,
                            "removed upstream but locally modified",
                        )
                    )

            elif in_base and in_theirs:
                if base_tree[relpath] == theirs_tree[relpath]:
                    continue  # identical blob, skip without fetching content
                base_content = gh.get_blob_content(base_tree[relpath])
                theirs_content = gh.get_blob_content(theirs_tree[relpath])
                if base_content == theirs_content:
                    continue
                if not in_local:
                    result.conflicts.append(
                        MergeConflict(
                            recipe_name,
                            relpath,
                            "modified upstream but missing locally",
                        )
                    )
                    continue
                with open(local_file, "rb") as f:
                    local_content = f.read()
                if local_content == theirs_content:
                    # Already manually applied upstream's change locally: nothing
                    # to merge, and no need to spawn git merge-file for it.
                    continue
                if _is_binary(base_content) or _is_binary(theirs_content):
                    result.conflicts.append(
                        MergeConflict(
                            recipe_name, relpath, "binary content, cannot auto-merge"
                        )
                    )
                    continue
                conflict = _three_way_merge_file(
                    local_file, base_content, theirs_content
                )
                if conflict:
                    result.conflicts.append(
                        MergeConflict(recipe_name, relpath, "merge conflict")
                    )
                else:
                    result.merged.append(relpath)
    return result


def run_conanmerge(
    repo_root: str,
    groups: typing.Sequence[str] = (),
    targets: typing.Sequence[str] = (),
    branch: str = constants.CCI_DEFAULT_BRANCH,
    force: bool = False,
) -> ConanMergeReport:
    if not groups and not targets:
        raise click.UsageError(
            "--merge requires --group/--target to scope which recipes to merge"
        )
    names = _resolve_recipe_names(groups, targets)
    data = load_upstream_data(repo_root)
    recipes = data.get("recipes", {})
    gh = CCIGitHub()
    report = ConanMergeReport()
    for name in sorted(names):
        entry = recipes.get(name)
        if entry is None or entry.get("class") != "cci":
            continue
        report.results.append(_merge_recipe(repo_root, gh, name, entry, branch, force))
    return report


# ---------------------------------------------------------------------------
# --merge --dry-run: preview what changed upstream (tracked SHA -> current
# upstream HEAD), without touching local files or attempting any merge.
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class FileDiff:
    recipe: str
    path: str
    status: str  # "added" | "removed" | "modified"
    diff: str


@dataclasses.dataclass
class ConanMergePreview:
    diffs: list = dataclasses.field(default_factory=list)


def _diff_lines(content: bytes) -> typing.List[str]:
    return content.decode("utf-8", errors="replace").splitlines(keepends=True)


def _preview_recipe_diff(  # pylint: disable=too-many-locals
    gh: CCIGitHub, recipe_name: str, entry: dict, branch: str
) -> typing.List[FileDiff]:
    diffs = []
    upstream_name = entry.get("upstream_name", recipe_name)
    new_ref_sha = gh.get_ref_sha(branch)
    for folder, sha in iter_folder_shas(entry):
        upstream_path = f"recipes/{upstream_name}/{folder}"
        base_tree = gh.get_tree_at_ref(upstream_path, sha)
        theirs_tree = gh.get_tree_at_ref(upstream_path, new_ref_sha)
        for relpath in sorted(set(base_tree) | set(theirs_tree)):
            in_base = relpath in base_tree
            in_theirs = relpath in theirs_tree
            if in_base and in_theirs and base_tree[relpath] == theirs_tree[relpath]:
                continue  # identical blob, skip without fetching content
            base_content = gh.get_blob_content(base_tree[relpath]) if in_base else b""
            theirs_content = (
                gh.get_blob_content(theirs_tree[relpath]) if in_theirs else b""
            )
            if base_content == theirs_content:
                continue
            status = (
                "modified"
                if in_base and in_theirs
                else ("added" if in_theirs else "removed")
            )
            path = f"{folder}/{relpath}"
            if _is_binary(base_content) or _is_binary(theirs_content):
                diffs.append(
                    FileDiff(recipe_name, path, status, "(binary file differs)")
                )
                continue
            diff_text = "".join(
                difflib.unified_diff(
                    _diff_lines(base_content),
                    _diff_lines(theirs_content),
                    fromfile=f"a/{relpath}@{sha[:12]}",
                    tofile=f"b/{relpath}@{new_ref_sha[:12]}",
                )
            )
            diffs.append(FileDiff(recipe_name, path, status, diff_text))
    return diffs


def run_conanmerge_preview(
    repo_root: str,
    groups: typing.Sequence[str] = (),
    targets: typing.Sequence[str] = (),
    branch: str = constants.CCI_DEFAULT_BRANCH,
) -> ConanMergePreview:
    if not groups and not targets:
        raise click.UsageError(
            "--merge --dry-run requires --group/--target to scope which recipes to preview"
        )
    names = _resolve_recipe_names(groups, targets)
    data = load_upstream_data(repo_root)
    recipes = data.get("recipes", {})
    gh = CCIGitHub()
    preview = ConanMergePreview()
    for name in sorted(names):
        entry = recipes.get(name)
        if entry is None or entry.get("class") != "cci":
            continue
        preview.diffs.extend(_preview_recipe_diff(gh, name, entry, branch))
    return preview


# ---------------------------------------------------------------------------
# --update-manifest
# ---------------------------------------------------------------------------


def run_update_manifest(  # pylint: disable=too-many-locals
    repo_root: str,
    groups: typing.Sequence[str] = (),
    targets: typing.Sequence[str] = (),
    branch: str = constants.CCI_DEFAULT_BRANCH,
    merge_report: typing.Optional[ConanMergeReport] = None,
) -> list:
    if not groups and not targets:
        raise click.UsageError(
            "--update-manifest requires --group/--target to scope which recipes to update"
        )
    names = _resolve_recipe_names(groups, targets)
    data = load_upstream_data(repo_root)
    recipes = data.get("recipes", {})
    gh = CCIGitHub()
    clean_recipes = merge_report.clean_recipes() if merge_report is not None else None
    updated = []
    for name in sorted(names):
        entry = recipes.get(name)
        if entry is None or entry.get("class") != "cci":
            continue
        if clean_recipes is not None and name not in clean_recipes:
            continue
        upstream_name = entry.get("upstream_name", name)
        folders = (
            list(entry["versions"].keys()) if "versions" in entry else [entry["folder"]]
        )
        for folder in folders:
            commit = gh.get_latest_folder_commit(
                f"recipes/{upstream_name}/{folder}", branch
            )
            if commit is None:
                continue
            new_sha = commit.sha
            if "versions" in entry:
                entry["versions"][folder]["sha"] = new_sha
            else:
                entry["sha"] = new_sha
        updated.append(name)
    save_upstream_data(repo_root, data)
    return updated
