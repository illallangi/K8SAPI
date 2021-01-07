from collections.abc import Mapping

from requests import request

from .apikind import APIKind


class APIKindCollection(Mapping):
    def __init__(self, *groups, **kwargs):
        super().__init__(**kwargs)
        self._items = dict({item.kind: item for item in self._load(*groups)})

    def _load(self, *groups):
        for group in groups:
            with request("get", group.rest_path) as r:
                for resource in r.json()["resources"]:
                    if "/" not in resource["name"]:
                        yield APIKind(group, resource)

    def __getitem__(self, k):
        return self._items.__getitem__(k)

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return self._items.__len__()
