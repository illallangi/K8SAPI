from re import Pattern, compile
from sys import stderr

from click import Choice as CHOICE, STRING, argument, group, option

from illallangi.k8sapi import API

from loguru import logger

from notifiers.logging import NotificationHandler


@group()
@option(
    "--log-level",
    type=CHOICE(
        ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "SUCCESS", "TRACE"],
        case_sensitive=False,
    ),
    default="DEBUG",
)
@option("--slack-webhook", type=STRING, envvar="SLACK_WEBHOOK", default=None)
@option("--slack-username", type=STRING, envvar="SLACK_USERNAME", default=__name__)
@option("--slack-format", type=STRING, envvar="SLACK_FORMAT", default="{message}")
def cli(log_level, slack_webhook, slack_username, slack_format):
    logger.remove()
    logger.add(stderr, level=log_level)

    if slack_webhook:
        params = {"username": slack_username, "webhook_url": slack_webhook}
        slack = NotificationHandler("slack", defaults=params)
        logger.add(slack, format=slack_format, level="SUCCESS")


@cli.command(name="get-api-groups")
@argument("group-filter", type=STRING, default="")
@argument("kind-filter", type=STRING, default="")
@option("--endpoint", type=STRING, default="http://localhost:8001")
def get_api_groups(endpoint, group_filter, kind_filter):
    api = API(endpoint)
    group_filter = (
        compile(group_filter) if not isinstance(group_filter, Pattern) else group_filter
    )
    kind_filter = (
        compile(kind_filter) if not isinstance(kind_filter, Pattern) else kind_filter
    )

    kinds = 0
    objects = 0
    filtered_groups = [
        group for group in api.groups.values() if group_filter.search(str(group))
    ]
    for api_group in filtered_groups:
        logger.info(f"{api_group}")

        filtered_kinds = [
            kind for kind in api_group.kinds.values() if kind_filter.search(str(kind))
        ]
        for api_kind in filtered_kinds:
            logger.info(f"  {api_kind}")
            kinds += 1
            objects += api_kind.item_count

    logger.info(f"{kinds} kinds, {objects} objects")


@cli.command(name="get-api-object")
@argument("kind", type=STRING)
@option("--endpoint", type=STRING, default="http://localhost:8001")
def get_api_object(endpoint, kind):
    api = API(endpoint)
    kind = api.kinds[kind]
    logger.info(kind)


@cli.command(name="get-api-object-url")
@argument("kind", type=STRING)
@option("--namespace", "-n", type=STRING, default="default")
@argument("name", type=STRING)
@option("--endpoint", type=STRING, default="http://localhost:8001")
def get_api_object_url(endpoint, kind, namespace, name):
    api = API(endpoint)
    kind = api.kinds[kind]
    logger.info(kind.calculate_url(namespace, name))


@cli.command(name="get-api-kinds")
@argument("kind-filter", type=STRING, default="")
@option("--endpoint", type=STRING, default="http://localhost:8001")
def get_api_kinds(endpoint, kind_filter):
    api = API(endpoint)
    kind_filter = (
        compile(kind_filter) if not isinstance(kind_filter, Pattern) else kind_filter
    )

    kinds = 0
    objects = 0
    filtered_kinds = [
        kind for kind in api.kinds.values() if kind_filter.search(str(kind))
    ]
    for api_kind in filtered_kinds:
        logger.info(f"{api_kind}")
        kinds += 1
        objects += api_kind.item_count

    logger.info(f"{kinds} kinds, {objects} objects")


if __name__ == "__main__":
    cli()
