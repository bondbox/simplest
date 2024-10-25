# coding:utf-8

from typing import Dict
from typing import Set

from xarg import singleton


class Node():
    def __init__(self, hostname: str):
        self.__hostname: str = hostname
        ROLES.get("all").add(self)

    @property
    def hostname(self) -> str:
        return self.__hostname


class NodeSet(Set[Node]):
    def __init__(self, setname: str):
        self.__setname: str = setname.lower()
        super().__init__()

    @property
    def setname(self) -> str:
        return self.__setname


@singleton
class Roles(Dict[str, NodeSet]):
    def __init__(self):
        super().__init__()

    def get(self, role: str) -> NodeSet:
        lname: str = role.lower()
        if lname not in self:
            self[lname] = NodeSet(lname)
        return self[lname]


@singleton
class Tags(Dict[str, NodeSet]):
    def __init__(self):
        super().__init__()

    def get(self, tag: str) -> NodeSet:
        lname: str = tag.lower()
        if lname not in self:
            self[lname] = NodeSet(lname)
        return self[lname]


NODES: NodeSet = NodeSet("all")
ROLES: Roles = Roles()
TAGS: Tags = Tags()
