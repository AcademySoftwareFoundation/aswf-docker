# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Main aswfdocker command line implementation using click
"""
import os
import sys
import logging
import click
import warnings

from aswfdocker import (
    builder,
    migrater,
    aswfinfo,
    groupinfo,
    constants,
    dockergen as aswf_dockergen,
    index,
    utils,
    releaser,
    settings as aswf_settings,
)

# Avoid pylint giving us grief for complex command lines
# pylint: disable=too-many-arguments

logger = logging.getLogger("build-images")


pass_build_info = click.make_pass_decorator(aswfinfo.ASWFInfo)


@click.group()
@click.option(
    "--repo-root",
    "-r",
    envvar="ASWF_REPO_ROOT",
    default=".",
    help="Root of aswf-docker repository",
)
@click.option("--repo-uri", "-u", help="URL of current Git Repository")
@click.option("--source-branch", "-b", help="Current git branch name")
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.version_option("1.0")
@click.pass_context
def cli(ctx, repo_root, repo_uri, source_branch, verbose):
    """aswfdocker is a command line interface to build ASWF Docker packages and CI images
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    ctx.obj = aswfinfo.ASWFInfo(
        repo_uri=repo_uri,
        source_branch=source_branch,
        repo_root=os.path.abspath(repo_root),
    )


def validate_image_name(ctx, param, value):  # noqa unused arguments error
    if value is None:
        return None
    try:
        return utils.get_image_spec(value)
    except RuntimeError as e:
        raise click.BadParameter(e.args[0])


def common_image_options(function):
    function = click.option(
        "--ci-image-type",
        "-t",
        required=False,
        help="Builds a ci-package or a ci-image.",
        type=click.Choice(constants.ImageType.__members__.keys(), case_sensitive=True),
    )(function)
    function = click.option(
        "--group",
        "-g",
        required=False,
        multiple=True,
        help='The name of the group of images to build, e.g. "base" or "vfx", can be specified multiple times.',
    )(function)
    function = click.option(
        "--version",
        "-v",
        required=False,
        multiple=True,
        help='The major version number to build, e.g. "2019", can be specified multiple times.',
    )(function)
    function = click.option(
        "--full-name",
        "-n",
        callback=validate_image_name,
        required=False,
        help="The full image name, e.g. aswftesting/ci-common:1 or aswf/ci-package-openexr:2019",
    )(function)
    function = click.option(
        "--target",
        "-tg",
        required=False,
        multiple=True,
        help='An optional package or image name to build, e.g. "usd", can be specified multiple times.',
    )(function)
    return function


def get_group_info(build_info, ci_image_type, groups, versions, full_name, targets):
    idx = index.Index()
    if full_name:
        org, image_type, target, version = full_name
        versions = [version]
        targets = [target]
        try:
            groups = [idx.get_group_from_image(image_type, target)]
        except RuntimeError as e:
            raise click.BadOptionUsage(option_name="--full-name", message=e.args[0])
        build_info.set_org(org)
    else:
        image_type = constants.ImageType[ci_image_type]
        if not groups and targets:
            groups = [idx.get_group_from_image(image_type, targets[0])]
    group_info = groupinfo.GroupInfo(
        type_=image_type, names=groups, versions=versions, targets=targets,
    )
    return group_info


@cli.command()
@common_image_options
@click.option(
    "--push",
    "-p",
    type=click.Choice(["YES", "NO", "AUTO"], case_sensitive=False),
    default="NO",
    help="Push built images to Docker repository.",
)
@click.option("--dry-run", "-d", is_flag=True, help="Just logs what would happen.")
@click.option(
    "--progress",
    "-pr",
    type=click.Choice(("auto", "tty", "plain"), case_sensitive=True),
    default="auto",
    help='Set type of progress output for "docker buildx bake" command.',
)
@pass_build_info
def build(
    build_info,
    ci_image_type,
    group,
    version,
    full_name,
    target,
    push,
    dry_run,
    progress,
):
    """Builds a ci-package or ci-image Docker image.
    """
    if push == "YES":
        pushb = True
    elif push == "AUTO":
        pushb = utils.get_docker_push(build_info.repo_uri, build_info.source_branch)
    else:
        pushb = False

    group_info = get_group_info(
        build_info, ci_image_type, group, version, full_name, target
    )
    b = builder.Builder(build_info=build_info, group_info=group_info, push=pushb)
    b.build(dry_run=dry_run, progress=progress)


@cli.command()
@click.option("--from", "-f", "from_org", default="aswftesting")
@click.option("--to", "-t", "to_org", default="aswf")
@click.option(
    "--package",
    "-p",
    help="Optional package name to migrate (all packages are migrated by default)",
)
@click.option(
    "--version",
    "-v",
    help="Version of the package to migrate (all versions are migrated by default)",
)
@click.option("--dry-run", "-d", is_flag=True)
def migrate(from_org, to_org, package, version, dry_run):
    """Migrates packages from a Docker Hub org to another.
    """
    m = migrater.Migrater(from_org, to_org)
    m.gather(package, version)
    if not click.confirm(
        "Are you sure you want to migrate the following {} packages?\n{}\n".format(
            len(m.migration_list),
            "\n".join(f"{mi.source} -> {mi.destination}" for mi in m.migration_list),
        )
    ):
        click.echo("Migration cancelled.")
        return
    m.migrate(dry_run)
    click.echo("Migration done.")


@cli.command()
@pass_build_info
def getdockerorg(build_info):
    """Prints the current Docker Hub organization to use according to the current repo uri and branch name
    """
    click.echo(
        utils.get_docker_org(build_info.repo_uri, build_info.source_branch), nl=False
    )


@cli.command()
@pass_build_info
def getdockerpush(build_info):
    """Prints if the images should be pushed according to the current repo uri and branch name
    """
    click.echo(
        "true"
        if utils.get_docker_push(build_info.repo_uri, build_info.source_branch)
        else "false",
        nl=False,
    )


@cli.command()
@click.option(
    "--docker-org", "-d", default="aswf", help="Docker organization",
)
@click.option(
    "--package", "-p", help="Package name to download",
)
@click.option(
    "--version", "-v", help="Package version to download",
)
@pass_build_info
def download(build_info, docker_org, package, version):
    """Downloads and extracts a ci-package into the packages folder.
    """
    path = utils.download_package(build_info.repo_root, docker_org, package, version)
    click.echo(path, nl=False)


@cli.command()
def packages():
    """Lists all known CI packages in this format: PACKAGEGROUP/ci-package-PACKAGE:VERSION
    """
    for group, packages in index.Index().groups[constants.ImageType.PACKAGE].items():
        for package in packages:
            image_name = utils.get_image_name(constants.ImageType.PACKAGE, package)
            for version in index.Index().iter_versions(
                constants.ImageType.PACKAGE, package
            ):
                click.echo(f"{group}/{image_name}:{version}")


@cli.command()
def images():
    """Lists all known CI images in this format: IMAGEGROUP/ci-IMAGE:VERSION
    """
    for group, images in index.Index().groups[constants.ImageType.IMAGE].items():
        for image in images:
            image_name = utils.get_image_name(constants.ImageType.IMAGE, image)
            for version in index.Index().iter_versions(
                constants.ImageType.IMAGE, image
            ):
                click.echo(f"{group}/{image_name}:{version}")


@cli.command()
@click.option(
    "--settings-path", "-p", default="~/.aswfdocker", help="User settings file path.",
)
@click.option(
    "--github-access-token",
    "-g",
    help="GitHub access token generated from https://github.com/settings/tokens",
)
def settings(settings_path, github_access_token):
    """Sets user settings
    """
    s = aswf_settings.Settings(settings_path=settings_path)
    s.github_access_token = github_access_token
    s.save()


@cli.command()
@common_image_options
@click.option(
    "--sha",
    "-s",
    help="The sha to create the release tag on, defaults to current sha.",
)
@click.option(
    "--github-org",
    "-o",
    default=constants.MAIN_GITHUB_ASWF_ORG,
    help=f"The GitHub organization/username to create the release on, defaults to {constants.MAIN_GITHUB_ASWF_ORG}.",
)
@click.option(
    "--docker-org",
    "-do",
    default=constants.TESTING_DOCKER_ORG,
    help=f"The Docker organization/username to upload the Docker image to, defaults to {constants.TESTING_DOCKER_ORG}.",
)
@click.option(
    "--message", "-m", help="The release message.",
)
@click.option("--dry-run", "-d", is_flag=True, help="Just logs what would happen.")
@pass_build_info
def release(
    build_info,
    ci_image_type,
    group,
    version,
    full_name,
    target,
    sha,
    github_org,
    docker_org,
    message,
    dry_run,
):
    """Creates a GitHub release for a ci-package or ci-image Docker image.
    """

    # Disable SSL unclosed ResourceWarning coming from GitHub
    warnings.filterwarnings(
        action="ignore", message="unclosed", category=ResourceWarning
    )

    if not sha:
        if utils.get_current_branch() != "master":
            click.secho(
                "Cannot release from non-master branch! Specify --sha to create a release on a given commit.",
                fg="red",
            )
            sys.exit(1)
        sha = utils.get_current_sha()
    if docker_org:
        build_info.docker_org = docker_org

    group_info = get_group_info(
        build_info, ci_image_type, group, version, full_name, target
    )

    r = releaser.Releaser(
        github_org=github_org,
        build_info=build_info,
        group_info=group_info,
        message=message,
        sha=sha,
    )
    r.gather()
    if not click.confirm(
        "Are you sure you want to create the following {} release on sha={}?\n{}\n".format(
            len(r.release_list), r.sha, "\n".join(tag for _, _, tag in r.release_list),
        )
    ):
        click.echo("Release cancelled.")
        return
    r.release(dry_run=dry_run)
    click.echo("Release done.")


@cli.command()
@click.pass_context
@click.option(
    "--image-name", "-n", default="all", help='Image name to generate. E.g. "base"'
)
@click.option(
    "--check", "-c", is_flag=True, help="Checks that the current files are up to date."
)
def dockergen(context, image_name, check):
    """Generates a Docker file and readme from image data and template
    """
    if image_name == "all":
        images = []
        for gimages in index.Index().groups[constants.ImageType.IMAGE].values():
            images.extend(gimages)
    else:
        images = [image_name]
    if check:
        for image in images:
            path, ok = aswf_dockergen.DockerGen(image).check_dockerfile()
            if not ok:
                click.secho(f"{path} is not up to date!", fg="red")
                context.exit(1)
            else:
                click.secho(f"{path} is up to date", fg="green")
            path, ok = aswf_dockergen.DockerGen(image).check_readme()
            if not ok:
                click.secho(f"{path} is not up to date!", fg="red")
                context.exit(1)
            else:
                click.secho(f"{path} is up to date", fg="green")
    else:
        for image in images:
            path = aswf_dockergen.DockerGen(image).generate_dockerfile()
            click.echo(f"Generated {path}")
            path = aswf_dockergen.DockerGen(image).generate_readme()
            click.echo(f"Generated {path}")


@cli.command()
@common_image_options
@click.option(
    "--username", "-u", help="Docker Hub username.",
)
@click.option(
    "--password", "-p", help="Docker Hub password",
)
@pass_build_info
def pushoverview(
    build_info, ci_image_type, group, version, full_name, target, username, password,
):
    """Pushes the Docker Image README file to Docker Hub
    """
    group_info = get_group_info(
        build_info, ci_image_type, group, version, full_name, target
    )
    if group_info.type == constants.ImageType.PACKAGE:
        click.echo("Package readme do not exist yet.")
        return
    token = utils.get_dockerhub_token(username, password)
    for image, _ in group_info.iter_images_versions():
        dg = aswf_dockergen.DockerGen(image.replace("ci-", ""))
        if dg.push_overview(build_info.docker_org, token):
            click.secho(
                f"Successfully pushed description to image {build_info.docker_org}/{image}",
                fg="green",
            )
        else:
            click.secho(
                f"Failed to push description to image {build_info.docker_org}/{image}",
                fg="red",
            )
            click.get_current_context().exit(1)
