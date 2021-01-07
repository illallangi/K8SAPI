from collections.abc import Mapping

from requests import request

from .apigroup import APIGroup


class APIGroupCollection(Mapping):
    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self._items = dict({item.group_version: item for item in self._load()})

    def _load(self):
        yield APIGroup(self.api, None, "v1")
        with request("get", self.api.endpoint / "apis") as r:
            for group in r.json()["groups"]:
                yield APIGroup(
                    self.api, group["name"], group["preferredVersion"]["version"]
                )

    def __getitem__(self, k):
        return self._items.__getitem__(k)

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return self._items.__len__()
