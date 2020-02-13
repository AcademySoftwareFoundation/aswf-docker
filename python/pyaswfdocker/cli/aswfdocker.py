import os
import logging
import subprocess
import click

from .. import builder, buildinfo, constants, utils


logger = logging.getLogger("build-images")


pass_build_info = click.make_pass_decorator(buildinfo.BuildInfo)


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
    ctx.obj = buildinfo.BuildInfo(
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
    type=click.Choice(constants.IMAGE_TYPE.__members__.keys(), case_sensitive=True),
)
@click.option("--group-name", "-g", required=True)
@click.option("--group-version", "-v", required=True)
@click.option("--target", "-tg", required=False)
@click.option("--push", "-p", is_flag=True)
@click.option("--dry-run", "-d", is_flag=True)
@click.option(
    "--progress",
    "-pr",
    type=click.Choice(("auto", "tty", "plain"), case_sensitive=True),
    default="auto",
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
        image_type=constants.IMAGE_TYPE[ci_image_type],
        group_name=group_name,
        group_version=group_version,
        target=target,
        push=push,
        dry_run=dry_run,
        progress=progress,
    )
    b.build()


@cli.command()
@click.option("--from", "-f", "from_org", default="aswftesting")
@click.option("--to", "-t", "to_org", default="aswf")
@click.option("--dry-run", "-d", is_flag=True)
def migrate(from_org, to_org, dry_run):
    for pkg, versions in constants.VERSIONS[constants.IMAGE_TYPE.PACKAGE].items():
        for version in versions:
            fromPkg = f"{from_org}/ci-package-{pkg}:{version}"
            toPkg = f"{to_org}/ci-package-{pkg}:{version}"
            logger.info("Migrating %s -> %s", fromPkg, toPkg)
            if not dry_run:
                subprocess.run(
                    f"docker pull {fromPkg}", shell=True, check=True,
                )
                subprocess.run(
                    f"docker tag {fromPkg} {toPkg}", shell=True, check=True,
                )
                subprocess.run(
                    f"docker push {toPkg}", shell=True, check=True,
                )

@cli.command()
@pass_build_info
def getdockerorg(build_info):
    click.echo(utils.get_docker_org(build_info.repo_uri, build_info.source_branch))
