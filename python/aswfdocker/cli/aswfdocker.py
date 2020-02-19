# SPDX-License-Identifier: Apache-2.0
"""
Main aswfdocker command line implementation using click
"""
import os
import logging
import click

from aswfdocker import builder, migrater, aswfinfo, constants, utils


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
    """aswfdocker is a command line interface to build ASWF Docker packages and ci images
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


@cli.command()
@click.option(
    "--ci-image-type",
    "-t",
    required=True,
    help="Builds a ci-package or a ci-image.",
    type=click.Choice(constants.ImageType.__members__.keys(), case_sensitive=True),
)
@click.option(
    "--group-name",
    "-g",
    required=True,
    help='The name of the group of images to build, e.g. "base" or "vfx".',
)
@click.option(
    "--group-version",
    "-v",
    required=True,
    help='The major version number to build, e.g. "2019".',
)
@click.option(
    "--target",
    "-tg",
    required=False,
    help='An optional package or image name to build, e.g. "usd".',
)
@click.option(
    "--push", "-p", is_flag=True, help="Push built images to docker repository."
)
@click.option("--dry-run", "-d", is_flag=True, help="Just logs what would happen.")
@click.option(
    "--progress",
    "-pr",  # noqa ignore too many arguments error
    type=click.Choice(("auto", "tty", "plain"), case_sensitive=True),
    default="auto",
    help='Set type of progress output for "docker buildx bake" command.',
)
@pass_build_info
def build(
    build_info,
    ci_image_type,
    group_name,
    group_version,
    target,
    push,
    dry_run,
    progress,
):
    """Builds a ci-package or ci-image docker image.
    """
    b = builder.Builder(
        build_info=build_info,
        group_info=builder.GroupInfo(
            type_=constants.ImageType[ci_image_type],
            name=group_name,
            version=group_version,
            target=target,
        ),
        push=push,
    )
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
    """Migrates packages from a dockerhub org to another.
    """
    m = migrater.Migrater(from_org, to_org)
    m.gather(package, version)
    if not click.confirm(
        "Are you sure you want to migrate the following {} packages?\n{}\n".format(
            len(m.migration_list),
            "\n".join(f"{mi.source} -> {mi.destination}" for mi in m.migration_list),
        )
    ):
        return
    m.migrate(dry_run)


@cli.command()
@pass_build_info
def getdockerorg(build_info):
    """Prints the current dockerhub organisation to use according to the current repo uri and branch name
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
        utils.get_docker_push(build_info.repo_uri, build_info.source_branch), nl=False
    )


@cli.command()
@click.option(
    "--docker-org", "-d", default="aswf", help="Docker organisation",
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
    """Lists all known ci packages in this format: PACKAGEGROUP/ci-package-PACKAGE:VERSION
    """
    for group, packages in constants.GROUPS[constants.ImageType.PACKAGE].items():
        for package in packages:
            image_name = utils.get_image_name(constants.ImageType.PACKAGE, package)
            for version in constants.VERSIONS[constants.ImageType.PACKAGE][package]:
                click.echo(f"{group}/{image_name}:{version}")


@cli.command()
def images():
    """Lists all known ci images in this format: IMAGEGROUP/ci-IMAGE:VERSION
    """
    for group, images in constants.GROUPS[constants.ImageType.IMAGE].items():
        for image in images:
            image_name = utils.get_image_name(constants.ImageType.IMAGE, image)
            for version in constants.VERSIONS[constants.ImageType.IMAGE][image]:
                click.echo(f"{group}/{image_name}:{version}")
