from cached_property import cached_property

from yarl import URL

from .apigroupcollection import APIGroupCollection
from .apikindcollection import APIKindCollection


class API(object):
    def __init__(self, endpoint="http://localhost:8001", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = URL(endpoint) if not isinstance(endpoint, URL) else endpoint

    def __repr__(self):
        return f"{self.__class__}({self.endpoint})"

    def __str__(self):
        return f"{self.endpoint}"

    @cached_property
    def groups(self):
        return APIGroupCollection(self)

    @cached_property
    def kinds(self):
        return APIKindCollection(*(self.groups.values()))
