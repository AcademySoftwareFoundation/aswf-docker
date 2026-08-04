# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# pylint: disable=protected-access

import os
import subprocess
import tempfile
import unittest
from unittest import mock

import click
from click.testing import CliRunner

from aswfdocker import conandiff
from aswfdocker.cli import aswfdocker


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(content, bytes) else "w"
    kwargs = {} if isinstance(content, bytes) else {"encoding": "utf-8"}
    with open(path, mode, **kwargs) as f:
        f.write(content)


def _git(repo_root, *args):
    subprocess.run(
        ["git", *args], cwd=repo_root, check=True, capture_output=True, text=True
    )


def _init_git_repo(repo_root):
    _git(repo_root, "init", "-q")
    _git(repo_root, "config", "user.email", "test@example.com")
    _git(repo_root, "config", "user.name", "Test")


def _commit_all(repo_root, message="init"):
    _git(repo_root, "add", "-A")
    _git(repo_root, "commit", "-q", "-m", message)


class _FakeCommit:
    def __init__(self, sha, message="msg"):
        self.sha = sha
        self.commit = mock.MagicMock()
        self.commit.author.date = "2024-01-01"
        self.commit.message = message


class _FakeCCIGitHub:
    """Test double for conandiff.CCIGitHub: no network access."""

    def __init__(self, new_ref_sha="NEWREF"):
        self.trees = {}  # {(path, ref): {relpath: blob_key}}
        self.blobs = {}  # {blob_key: bytes}
        self.folder_commits = {}  # {(path, ref): [commit, ...]}
        self.commit_for_sha = {}  # {(path, sha): commit or None}
        self.config_ymls = {}  # {(upstream_name, ref): dict or None}
        self.new_ref_sha = new_ref_sha
        self.repo = mock.MagicMock()
        self.repo.get_commit.return_value.sha = new_ref_sha

    def get_ref_sha(self, ref):  # pylint: disable=unused-argument
        return self.new_ref_sha

    def get_tree_at_ref(self, path, ref):
        return dict(self.trees.get((path, ref), {}))

    def get_blob_content(self, blob_sha):
        return self.blobs[blob_sha]

    def get_folder_commits(self, path, ref):
        return list(self.folder_commits.get((path, ref), []))

    def get_latest_folder_commit(self, path, ref):
        commits = self.folder_commits.get((path, ref), [])
        return commits[0] if commits else None

    def get_commit_for_sha(self, path, sha):
        return self.commit_for_sha.get((path, sha))

    def get_config_yml_versions(self, upstream_name, ref):
        return self.config_ymls.get((upstream_name, ref))

    def folder_exists(
        self, upstream_name, folder, ref
    ):  # pylint: disable=unused-argument
        return True


def _fake_content_item(name, sha, item_type, path=None):
    item = mock.MagicMock()
    item.name = name
    item.sha = sha
    item.type = item_type
    item.path = path or name
    return item


def _fake_tree_entry(path, sha, entry_type="blob"):
    entry = mock.MagicMock()
    entry.path = path
    entry.sha = sha
    entry.type = entry_type
    return entry


def _real_cci_github_no_network():
    """A real CCIGitHub with .repo mocked out, bypassing __init__'s network call."""
    gh = conandiff.CCIGitHub.__new__(conandiff.CCIGitHub)
    gh.repo = mock.MagicMock()
    gh._commit_sha_cache = {}  # pylint: disable=protected-access
    gh._blob_cache = {}  # pylint: disable=protected-access
    return gh


class TestCCIGitHubScopingAndCaching(unittest.TestCase):
    """Real CCIGitHub, but with .repo mocked out: no network access."""

    def _gh(self):
        return _real_cci_github_no_network()

    def test_tree_scoped_to_folder_not_whole_repo(self):
        gh = self._gh()
        test_package_sha = "tp" * 20
        gh.repo.get_contents.return_value = [
            _fake_content_item("conanfile.py", "a" * 40, "file"),
            _fake_content_item("test_package", test_package_sha, "dir"),
        ]
        subtree = mock.MagicMock()
        subtree.tree = [_fake_tree_entry("CMakeLists.txt", "b" * 40)]
        gh.repo.get_git_tree.return_value = subtree

        result = gh.get_tree_at_ref("recipes/zlib/all", "master")

        gh.repo.get_contents.assert_called_once_with("recipes/zlib/all", ref="master")
        # Scoped to the subdirectory's own tree sha, never the repo/commit root.
        gh.repo.get_git_tree.assert_called_once_with(test_package_sha, recursive=True)
        self.assertEqual(
            result,
            {"conanfile.py": "a" * 40, "test_package/CMakeLists.txt": "b" * 40},
        )

    def test_get_ref_sha_is_cached(self):
        gh = self._gh()
        gh.repo.get_commit.return_value.sha = "resolved" * 5
        sha1 = gh.get_ref_sha("master")
        sha2 = gh.get_ref_sha("master")
        self.assertEqual(sha1, sha2)
        gh.repo.get_commit.assert_called_once_with("master")

    def test_get_blob_content_is_cached(self):
        gh = self._gh()
        gh.repo.get_git_blob.return_value.content = "aGVsbG8="  # base64("hello")
        content1 = gh.get_blob_content("someblobsha")
        content2 = gh.get_blob_content("someblobsha")
        self.assertEqual(content1, b"hello")
        self.assertEqual(content2, b"hello")
        gh.repo.get_git_blob.assert_called_once_with("someblobsha")


class _NoLenPaginatedList:
    """Simulates PyGithub's PaginatedList: lazily iterable, but len()/list()
    must never be called on it — that would force walking a path's *entire*
    commit history (real regression: used to happen via `list(...)`)."""

    def __init__(self, items):
        self._items = items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        raise AssertionError(
            "must not call len()/list() on paginated commits — would walk full history"
        )


class TestNoFullHistoryPagination(unittest.TestCase):
    """Real CCIGitHub/check_recipe, but with .repo mocked out: no network access."""

    def _gh(self):
        return _real_cci_github_no_network()

    def test_get_commit_for_sha_does_not_materialize_full_history(self):
        gh = self._gh()
        commits = [_FakeCommit(f"sha{i}") for i in range(500)]
        gh.repo.get_commits.return_value = _NoLenPaginatedList(commits)
        result = gh.get_commit_for_sha("recipes/yaml-cpp/all", "shaX")
        self.assertEqual(result.sha, "sha0")

    def test_get_latest_folder_commit_does_not_materialize_full_history(self):
        gh = self._gh()
        commits = [_FakeCommit(f"sha{i}") for i in range(500)]
        gh.repo.get_commits.return_value = _NoLenPaginatedList(commits)
        result = gh.get_latest_folder_commit("recipes/yaml-cpp/all", "master")
        self.assertEqual(result.sha, "sha0")

    def test_check_recipe_does_not_materialize_full_history(self):
        gh = self._gh()
        tracked = _FakeCommit("TRACKED")
        newer = [_FakeCommit(f"NEW{i}") for i in range(3)]
        # A long tail after the tracked commit that must never be touched:
        # if check_recipe (or get_folder_commits) ever called list()/len() on
        # this, __len__ raises and the test fails.
        ancient_history = [_FakeCommit(f"OLD{i}") for i in range(500)]

        def fake_get_commits(path, sha):  # pylint: disable=unused-argument
            if sha == "TRACKED":
                return _NoLenPaginatedList([tracked])
            return _NoLenPaginatedList(newer + [tracked] + ancient_history)

        gh.repo.get_commits.side_effect = fake_get_commits
        outdated, errors = conandiff.check_recipe(
            gh,
            "yaml-cpp",
            {"class": "cci", "folder": "all", "sha": "TRACKED"},
            "master",
        )
        self.assertEqual(errors, [])
        self.assertEqual(len(outdated), 1)
        self.assertEqual(
            [c.sha for c in outdated[0].newer_commits], ["NEW0", "NEW1", "NEW2"]
        )

    def test_run_update_manifest_does_not_materialize_full_history(self):
        gh = self._gh()
        commits = [_FakeCommit(f"sha{i}") for i in range(500)]
        gh.repo.get_commits.return_value = _NoLenPaginatedList(commits)
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"yaml-cpp": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            with mock.patch.object(conandiff, "CCIGitHub", return_value=gh):
                updated = conandiff.run_update_manifest(tmp, targets=["yaml-cpp"])
            self.assertEqual(updated, ["yaml-cpp"])
            new_data = conandiff.load_upstream_data(tmp)
            self.assertEqual(new_data["recipes"]["yaml-cpp"]["sha"], "sha0")


class TestResolveRecipeNames(unittest.TestCase):
    def test_no_scope_returns_everything(self):
        names = conandiff._resolve_recipe_names([], [])
        self.assertIn("zlib", names)
        self.assertIn("b2", names)

    def test_target_alone_autoresolves_group(self):
        names = conandiff._resolve_recipe_names([], ["zlib"])
        self.assertEqual(names, ["zlib"])

    def test_unknown_group_raises(self):
        with self.assertRaises(click.BadOptionUsage):
            conandiff._resolve_recipe_names(["not-a-real-group"], [])

    def test_group_and_target_combined(self):
        names = conandiff._resolve_recipe_names(["base1-1"], ["zlib", "b2"])
        self.assertEqual(sorted(names), ["b2", "zlib"])


class TestIterFolderShas(unittest.TestCase):
    def test_single_version(self):
        entry = {"class": "cci", "folder": "all", "sha": "abc"}
        self.assertEqual(list(conandiff.iter_folder_shas(entry)), [("all", "abc")])

    def test_multi_version(self):
        entry = {
            "class": "cci",
            "versions": {"5.x.x": {"sha": "aaa"}, "6.x.x": {"sha": "bbb"}},
        }
        self.assertEqual(
            sorted(conandiff.iter_folder_shas(entry)),
            [("5.x.x", "aaa"), ("6.x.x", "bbb")],
        )

    def test_non_cci_yields_nothing(self):
        self.assertEqual(list(conandiff.iter_folder_shas({"class": "unique"})), [])


class TestCheckRecipe(unittest.TestCase):
    def test_up_to_date(self):
        gh = _FakeCCIGitHub()
        gh.commit_for_sha[("recipes/zlib/all", "OLD")] = _FakeCommit("OLD")
        gh.folder_commits[("recipes/zlib/all", "master")] = [_FakeCommit("OLD")]
        entry = {"class": "cci", "folder": "all", "sha": "OLD"}
        outdated, errors = conandiff.check_recipe(gh, "zlib", entry, "master")
        self.assertEqual(outdated, [])
        self.assertEqual(errors, [])

    def test_finds_and_stops_at_tracked_sha(self):
        gh = _FakeCCIGitHub()
        gh.commit_for_sha[("recipes/zlib/all", "OLD")] = _FakeCommit("OLD")
        gh.folder_commits[("recipes/zlib/all", "master")] = [
            _FakeCommit("NEW2"),
            _FakeCommit("NEW1"),
            _FakeCommit("OLD"),
            _FakeCommit("OLDER"),
        ]
        entry = {"class": "cci", "folder": "all", "sha": "OLD"}
        outdated, errors = conandiff.check_recipe(gh, "zlib", entry, "master")
        self.assertEqual(len(outdated), 1)
        self.assertEqual([c.sha for c in outdated[0].newer_commits], ["NEW2", "NEW1"])
        self.assertEqual(errors, [])

    def test_tracked_sha_missing_is_error_not_crash(self):
        gh = _FakeCCIGitHub()
        # no entry in commit_for_sha -> None
        entry = {"class": "cci", "folder": "all", "sha": "GONE"}
        outdated, errors = conandiff.check_recipe(gh, "zlib", entry, "master")
        self.assertEqual(outdated, [])
        self.assertEqual(len(errors), 1)


class TestCheckRemovedVersions(unittest.TestCase):
    def _entry(self):
        return {
            "class": "cci",
            "versions": {"2020.x": {"sha": "aaa"}, "all": {"sha": "bbb"}},
        }

    def test_normal_all_present(self):
        gh = _FakeCCIGitHub()
        gh.config_ymls[("onetbb", "master")] = {
            "versions": {"1.0": {"folder": "2020.x"}, "2.0": {"folder": "all"}}
        }
        removed = conandiff.check_removed_versions(
            gh, "onetbb", self._entry(), "master"
        )
        self.assertEqual(removed, [])

    def test_folder_no_longer_referenced(self):
        gh = _FakeCCIGitHub()
        gh.config_ymls[("onetbb", "master")] = {"versions": {"2.0": {"folder": "all"}}}
        removed = conandiff.check_removed_versions(
            gh, "onetbb", self._entry(), "master"
        )
        self.assertEqual(len(removed), 1)
        self.assertEqual(removed[0].folder, "2020.x")

    def test_config_yml_missing_upstream_flags_everything(self):
        gh = _FakeCCIGitHub()
        gh.config_ymls[("onetbb", "master")] = None
        removed = conandiff.check_removed_versions(
            gh, "onetbb", self._entry(), "master"
        )
        self.assertEqual({r.folder for r in removed}, {"2020.x", "all"})


class TestRunConandiff(unittest.TestCase):
    def test_only_touches_network_for_cci_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {
                    "zlib": {"class": "cci", "folder": "all", "sha": "OLD"},
                    "b2": {"class": "unique"},
                    "cppunit": {"class": "system"},
                }
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.commit_for_sha[("recipes/zlib/all", "OLD")] = _FakeCommit("OLD")
            fake_gh.folder_commits[("recipes/zlib/all", "master")] = [
                _FakeCommit("OLD")
            ]
            with mock.patch.object(
                conandiff, "CCIGitHub", return_value=fake_gh
            ) as ctor:
                report = conandiff.run_conandiff(
                    tmp, targets=["zlib", "b2", "cppunit"], branch="master"
                )
            ctor.assert_called_once()
            self.assertEqual(report.outdated, [])
            self.assertEqual(report.errors, [])


class TestRunConanmerge(unittest.TestCase):
    def _recipes_dir(self, repo_root, name):
        return os.path.join(repo_root, "packages", "conan", "recipes", name)

    def test_unscoped_raises_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            conandiff.save_upstream_data(tmp, {"recipes": {}})
            with self.assertRaises(click.UsageError):
                conandiff.run_conanmerge(tmp, groups=[], targets=[])

    def test_dirty_tree_guard_skips_unless_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_git_repo(tmp)
            recipe_dir = self._recipes_dir(tmp, "zlib")
            _write(os.path.join(recipe_dir, "conanfile.py"), "content\n")
            _commit_all(tmp)
            # dirty it
            _write(os.path.join(recipe_dir, "conanfile.py"), "modified uncommitted\n")

            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                report = conandiff.run_conanmerge(tmp, targets=["zlib"])
            self.assertEqual(len(report.results), 1)
            self.assertTrue(report.results[0].skipped_reason)
            self.assertFalse(report.results[0].clean)

            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                report = conandiff.run_conanmerge(tmp, targets=["zlib"], force=True)
            # with force, it proceeds (no tree data configured -> just no-op, no conflicts)
            self.assertEqual(report.results[0].skipped_reason, "")

    def test_merge_scenarios(
        self,
    ):  # pylint: disable=too-many-locals,too-many-statements
        with tempfile.TemporaryDirectory() as tmp:
            _init_git_repo(tmp)

            # zlib: clean merge + an upstream-added file
            zlib_dir = self._recipes_dir(tmp, "zlib")
            zlib_base = b"A\nB\nX\nY\nZ\nC\n"
            zlib_theirs = b"A\nB\nX\nY\nZ\nC2\n"
            _write(os.path.join(zlib_dir, "conanfile.py"), b"A\nB2\nX\nY\nZ\nC\n")

            # b2: conflicting merge
            b2_dir = self._recipes_dir(tmp, "b2")
            b2_base = b"A\nB\nC\n"
            b2_theirs = b"A\nTHEIRS\nC\n"
            _write(os.path.join(b2_dir, "conanfile.py"), b"A\nOURS\nC\n")

            # cppunit: removed upstream, untouched locally -> deleted
            cppunit_dir = self._recipes_dir(tmp, "cppunit")
            cppunit_base = b"same content\n"
            _write(os.path.join(cppunit_dir, "conanfile.py"), cppunit_base)
            _write(os.path.join(cppunit_dir, "oldfile.txt"), cppunit_base)

            # eigen: removed upstream, but locally modified -> conflict, kept
            eigen_dir = self._recipes_dir(tmp, "eigen")
            eigen_base = b"original\n"
            _write(os.path.join(eigen_dir, "conanfile.py"), b"keep me\n")
            _write(os.path.join(eigen_dir, "oldfile.txt"), b"locally modified\n")

            _commit_all(tmp)

            data = {
                "recipes": {
                    "zlib": {"class": "cci", "folder": "all", "sha": "OLD"},
                    "b2": {"class": "cci", "folder": "all", "sha": "OLD"},
                    "cppunit": {"class": "cci", "folder": "all", "sha": "OLD"},
                    "eigen": {"class": "cci", "folder": "all", "sha": "OLD"},
                }
            }
            conandiff.save_upstream_data(tmp, data)

            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"conanfile.py": "zlib_base"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {
                "conanfile.py": "zlib_theirs",
                "newfile.txt": "zlib_newfile",
            }
            fake_gh.blobs["zlib_base"] = zlib_base
            fake_gh.blobs["zlib_theirs"] = zlib_theirs
            fake_gh.blobs["zlib_newfile"] = b"added upstream\n"

            fake_gh.trees[("recipes/b2/all", "OLD")] = {"conanfile.py": "b2_base"}
            fake_gh.trees[("recipes/b2/all", "NEWREF")] = {"conanfile.py": "b2_theirs"}
            fake_gh.blobs["b2_base"] = b2_base
            fake_gh.blobs["b2_theirs"] = b2_theirs

            fake_gh.trees[("recipes/cppunit/all", "OLD")] = {
                "conanfile.py": "cppunit_base",
                "oldfile.txt": "cppunit_base",
            }
            fake_gh.trees[("recipes/cppunit/all", "NEWREF")] = {
                "conanfile.py": "cppunit_base"
            }
            fake_gh.blobs["cppunit_base"] = cppunit_base

            fake_gh.trees[("recipes/eigen/all", "OLD")] = {
                "conanfile.py": "eigen_conanfile_base",
                "oldfile.txt": "eigen_base",
            }
            fake_gh.trees[("recipes/eigen/all", "NEWREF")] = {
                "conanfile.py": "eigen_conanfile_base"
            }
            fake_gh.blobs["eigen_conanfile_base"] = b"keep me\n"
            fake_gh.blobs["eigen_base"] = eigen_base

            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                report = conandiff.run_conanmerge(
                    tmp, targets=["zlib", "b2", "cppunit", "eigen"]
                )

            results = {r.recipe: r for r in report.results}

            self.assertEqual(results["zlib"].conflicts, [])
            self.assertIn("conanfile.py", results["zlib"].merged)
            self.assertIn("newfile.txt", results["zlib"].added)
            self.assertTrue(results["zlib"].clean)
            with open(os.path.join(zlib_dir, "conanfile.py"), "rb") as f:
                self.assertEqual(f.read(), b"A\nB2\nX\nY\nZ\nC2\n")

            self.assertEqual(len(results["b2"].conflicts), 1)
            self.assertFalse(results["b2"].clean)
            with open(os.path.join(b2_dir, "conanfile.py"), "r", encoding="utf-8") as f:
                merged_content = f.read()
            self.assertIn("<<<<<<<", merged_content)
            self.assertIn(">>>>>>>", merged_content)

            self.assertIn("oldfile.txt", results["cppunit"].removed)
            self.assertFalse(os.path.exists(os.path.join(cppunit_dir, "oldfile.txt")))
            self.assertTrue(results["cppunit"].clean)

            self.assertEqual(len(results["eigen"].conflicts), 1)
            self.assertFalse(results["eigen"].clean)
            self.assertTrue(os.path.exists(os.path.join(eigen_dir, "oldfile.txt")))
            with open(os.path.join(eigen_dir, "oldfile.txt"), "rb") as f:
                self.assertEqual(f.read(), b"locally modified\n")

            self.assertEqual(report.clean_recipes(), {"zlib", "cppunit"})

    def test_binary_content_flagged_without_merge_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_git_repo(tmp)
            expat_dir = self._recipes_dir(tmp, "expat")
            _write(os.path.join(expat_dir, "conanfile.py"), b"ours binary safe text\n")
            _commit_all(tmp)

            data = {
                "recipes": {"expat": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)

            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/expat/all", "OLD")] = {"conanfile.py": "expat_base"}
            fake_gh.trees[("recipes/expat/all", "NEWREF")] = {
                "conanfile.py": "expat_theirs"
            }
            fake_gh.blobs["expat_base"] = b"base\x00binary\n"
            fake_gh.blobs["expat_theirs"] = b"theirs binary safe text\n"

            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                report = conandiff.run_conanmerge(tmp, targets=["expat"])

            self.assertEqual(len(report.results[0].conflicts), 1)
            self.assertIn("binary", report.results[0].conflicts[0].reason)


class TestRunConanmergePreview(unittest.TestCase):
    def test_unscoped_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            conandiff.save_upstream_data(tmp, {"recipes": {}})
            with self.assertRaises(click.UsageError):
                conandiff.run_conanmerge_preview(tmp, groups=[], targets=[])

    def test_no_writes_to_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"conanfile.py": "base"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {"conanfile.py": "theirs"}
            fake_gh.blobs["base"] = b"A\nB\n"
            fake_gh.blobs["theirs"] = b"A\nB2\n"
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                conandiff.run_conanmerge_preview(tmp, targets=["zlib"])
            recipe_dir = os.path.join(tmp, "packages", "conan", "recipes", "zlib")
            self.assertFalse(os.path.exists(recipe_dir))

    def test_modified_file_shows_unified_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"conanfile.py": "base"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {"conanfile.py": "theirs"}
            fake_gh.blobs["base"] = b"A\nB\n"
            fake_gh.blobs["theirs"] = b"A\nB2\n"
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                preview = conandiff.run_conanmerge_preview(tmp, targets=["zlib"])
            self.assertEqual(len(preview.diffs), 1)
            d = preview.diffs[0]
            self.assertEqual(d.status, "modified")
            self.assertIn("-B", d.diff)
            self.assertIn("+B2", d.diff)

    def test_identical_blob_skips_fetch(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"conanfile.py": "same_blob"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {
                "conanfile.py": "same_blob"
            }
            # no blob content registered on purpose: a fetch would KeyError
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                preview = conandiff.run_conanmerge_preview(tmp, targets=["zlib"])
            self.assertEqual(preview.diffs, [])

    def test_added_and_removed_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"gone.txt": "gone_blob"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {"new.txt": "new_blob"}
            fake_gh.blobs["gone_blob"] = b"old content\n"
            fake_gh.blobs["new_blob"] = b"new content\n"
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                preview = conandiff.run_conanmerge_preview(tmp, targets=["zlib"])
            statuses = {d.path: d.status for d in preview.diffs}
            self.assertEqual(
                statuses, {"all/gone.txt": "removed", "all/new.txt": "added"}
            )

    def test_binary_flagged_without_diffing(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"conanfile.py": "base"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {"conanfile.py": "theirs"}
            fake_gh.blobs["base"] = b"a\x00b"
            fake_gh.blobs["theirs"] = b"a\x00c"
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                preview = conandiff.run_conanmerge_preview(tmp, targets=["zlib"])
            self.assertEqual(preview.diffs[0].diff, "(binary file differs)")


class TestRunUpdateManifest(unittest.TestCase):
    def test_standalone_bumps_unconditionally(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.folder_commits[("recipes/zlib/all", "master")] = [
                _FakeCommit("BRAND_NEW")
            ]
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                updated = conandiff.run_update_manifest(tmp, targets=["zlib"])
            self.assertEqual(updated, ["zlib"])
            new_data = conandiff.load_upstream_data(tmp)
            self.assertEqual(new_data["recipes"]["zlib"]["sha"], "BRAND_NEW")

    def test_with_merge_report_only_bumps_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {
                    "zlib": {"class": "cci", "folder": "all", "sha": "OLD_ZLIB"},
                    "b2": {"class": "cci", "folder": "all", "sha": "OLD_B2"},
                }
            }
            conandiff.save_upstream_data(tmp, data)
            fake_gh = _FakeCCIGitHub()
            fake_gh.folder_commits[("recipes/zlib/all", "master")] = [
                _FakeCommit("NEW_ZLIB")
            ]
            fake_gh.folder_commits[("recipes/b2/all", "master")] = [
                _FakeCommit("NEW_B2")
            ]

            merge_report = conandiff.ConanMergeReport(
                results=[
                    conandiff.RecipeMergeResult(recipe="zlib"),
                    conandiff.RecipeMergeResult(
                        recipe="b2",
                        conflicts=[
                            conandiff.MergeConflict(
                                "b2", "conanfile.py", "merge conflict"
                            )
                        ],
                    ),
                ]
            )
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                updated = conandiff.run_update_manifest(
                    tmp, targets=["zlib", "b2"], merge_report=merge_report
                )
            self.assertEqual(updated, ["zlib"])
            new_data = conandiff.load_upstream_data(tmp)
            self.assertEqual(new_data["recipes"]["zlib"]["sha"], "NEW_ZLIB")
            self.assertEqual(new_data["recipes"]["b2"]["sha"], "OLD_B2")

    def test_unscoped_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            conandiff.save_upstream_data(tmp, {"recipes": {}})
            with self.assertRaises(click.UsageError):
                conandiff.run_update_manifest(tmp)


class TestJsonRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = {
                "recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "abc"}}
            }
            conandiff.save_upstream_data(tmp, data)
            self.assertEqual(conandiff.load_upstream_data(tmp), data)

    def test_missing_file_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                conandiff.load_upstream_data(tmp)


class TestConandiffCli(unittest.TestCase):
    def _init_repo(self, tmp):
        conandiff.save_upstream_data(
            tmp, {"recipes": {"zlib": {"class": "cci", "folder": "all", "sha": "OLD"}}}
        )
        _write(
            os.path.join(tmp, "packages", "conan", "recipes", "zlib", "conanfile.py"),
            "content\n",
        )

    def test_plain_run_exit_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            fake_gh = _FakeCCIGitHub()
            fake_gh.commit_for_sha[("recipes/zlib/all", "OLD")] = _FakeCommit("OLD")
            fake_gh.folder_commits[("recipes/zlib/all", "master")] = [
                _FakeCommit("OLD")
            ]
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                runner = CliRunner()
                result = runner.invoke(
                    aswfdocker.cli, ["-r", tmp, "conandiff", "--target", "zlib"]
                )
            self.assertEqual(result.exit_code, 0, msg=result.output)
            self.assertIn("up to date", result.output)

    def test_unscoped_merge_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            runner = CliRunner()
            result = runner.invoke(aswfdocker.cli, ["-r", tmp, "conandiff", "--merge"])
            self.assertNotEqual(result.exit_code, 0)

    def test_merge_dry_run_shows_upstream_diff_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._init_repo(tmp)
            fake_gh = _FakeCCIGitHub()
            fake_gh.trees[("recipes/zlib/all", "OLD")] = {"conanfile.py": "base"}
            fake_gh.trees[("recipes/zlib/all", "NEWREF")] = {"conanfile.py": "theirs"}
            fake_gh.blobs["base"] = b"A\nB\n"
            fake_gh.blobs["theirs"] = b"A\nB2\n"
            with mock.patch.object(conandiff, "CCIGitHub", return_value=fake_gh):
                runner = CliRunner()
                result = runner.invoke(
                    aswfdocker.cli,
                    [
                        "-r",
                        tmp,
                        "conandiff",
                        "--merge",
                        "--dry-run",
                        "--target",
                        "zlib",
                    ],
                )
            self.assertEqual(result.exit_code, 0, msg=result.output)
            self.assertIn("-B", result.output)
            self.assertIn("+B2", result.output)
            recipe_dir = os.path.join(tmp, "packages", "conan", "recipes", "zlib")
            with open(
                os.path.join(recipe_dir, "conanfile.py"), "r", encoding="utf-8"
            ) as f:
                self.assertEqual(f.read(), "content\n")


if __name__ == "__main__":
    unittest.main()
