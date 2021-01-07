from cached_property import cached_property

from .apikindcollection import APIKindCollection


class APIGroup(object):
    def __init__(self, api, name, version, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self.name = name
        self.version = version

    def __repr__(self):
        return f"{self.__class__}({self.group_version} ({self.rest_path}))"

    def __str__(self):
        return f"{self.group_version} ({self.rest_path})"

    @cached_property
    def kinds(self):
        return APIKindCollection(self)

    @cached_property
    def group_version(self):
        if self.name:
            return f"{self.name}/{self.version}"
        return self.version

    @cached_property
    def rest_path(self):
        if self.name:
            return self.api.endpoint / "apis" / self.name / self.version
        return self.api.endpoint / "api" / self.version
