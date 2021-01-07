from cached_property import cached_property

from loguru import logger

from requests import request


class APIKind(object):
    def __init__(self, api_group, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_group = api_group
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                logger.error(
                    f'Unhandled key in {self.__class__}: {key}: {type(self._dictionary[key])}"{self._dictionary[key]}"'
                )
                continue
            logger.trace(
                f'{key}: {type(self._dictionary[key])}"{self._dictionary[key]}"'
            )

    @property
    def _keys(self):
        return [
            "name",
            "namespaced",
            "singularName",
            "kind",
            "verbs",
            "shortNames",
            "storageVersionHash",
            "categories",
            "group",
            "version",
        ]

    def __repr__(self):
        return f"{self.__class__}{self.kind} ({self.rest_path})"

    def __str__(self):
        return f"{self.kind} ({self.item_count} item(s))"

    @cached_property
    def name(self):
        return self._dictionary["name"]

    @cached_property
    def namespaced(self):
        return self._dictionary["namespaced"]

    @cached_property
    def singular_name(self):
        return self._dictionary["singularName"]

    @cached_property
    def kind(self):
        return self._dictionary["kind"]

    @cached_property
    def verbs(self):
        return self._dictionary["verbs"]

    @cached_property
    def short_names(self):
        return self._dictionary["shortNames"]

    @cached_property
    def storage_version_hash(self):
        return self._dictionary["storageVersionHash"]

    @cached_property
    def categories(self):
        return self._dictionary["categories"]

    @cached_property
    def group(self):
        return self._dictionary["group"]

    @cached_property
    def version(self):
        return self._dictionary["version"]

    @cached_property
    def rest_path(self):
        return self.api_group.rest_path / self.name

    @cached_property
    def item_count(self):
        with request("get", self.rest_path) as r:
            return len(r.json().get("items", []))

    def calculate_url(self, namespace, name):
        if self.namespaced:
            return (
                self.api_group.rest_path / "namespaces" / namespace / self.name / name
            )
        return self.api_group.rest_path / self.name / name
