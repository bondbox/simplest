# coding:utf-8

from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set

LABELTYPE = Optional[Iterable[str]]


class Node():
    def __init__(self, hostname: str, address: str):
        self.__hostname: str = hostname
        self.__address: str = address

    @property
    def hostname(self) -> str:
        return self.__hostname

    @property
    def address(self) -> str:
        return self.__address


class NodeSet(Set[Node]):
    def __init__(self, label: str):
        self.__label: str = label.lower()
        super().__init__()

    @property
    def label(self) -> str:
        return self.__label


class NodeGroup(Dict[str, NodeSet]):
    def __init__(self):
        super().__init__()

    def get(self, label: str) -> NodeSet:
        lower: str = label.lower()
        if lower not in self:
            self.setdefault(lower, NodeSet(lower))
        return self[lower]

    def add(self, node: Node, lables: Iterable[str]) -> List[NodeSet]:
        all_lables: Set[str] = set({n.lower() for n in lables}) | {"all"}
        all_groups: List[NodeSet] = list(self.get(a) for a in all_lables)
        for nodeset in all_groups:
            nodeset.add(node)
        return all_groups


class Nodes(Dict[str, Node]):
    def __init__(self):
        self.__roles: NodeGroup = NodeGroup()
        self.__tags: NodeGroup = NodeGroup()
        super().__init__()

    @property
    def roles(self) -> NodeGroup:
        return self.__roles

    @property
    def tags(self) -> NodeGroup:
        return self.__tags

    def get(self, hostname: str) -> Node:
        lower: str = hostname.lower()
        return self[lower]

    def add(self, node: Node, roles: LABELTYPE = None, tags: LABELTYPE = None):
        self.roles.add(node=node, lables=roles or {"all"})
        self.tags.add(node=node, lables=tags or {"all"})
        self.setdefault(node.hostname, node)

    def parse(self, lable: str) -> Node:
        """parse hostname and label

        Label Format:
                             ┏━  role  ━━┓ ┏━  tag  ━┓
        node-1,node-2,node-3@linux,storage:lvm,zfs,nfs
        ┗━━━  hostname  ━━━┛ ┗━━━━━━━  label  ━━━━━━━┛

        Example:
         - node-1@linux,storage:lvm,zfs,nfs
         - node-1@linux,storage
         - node-1@:lvm,zfs,nfs
         - linux,storage:nfs
         - linux,storage
         - :nfs(all:nfs)
        """
        pass
