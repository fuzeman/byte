from byte.core.models.nodes.base import Node


class Set(Node):
    def __init__(self, *nodes, **kwargs):
        """Create node set.

        :param nodes: Nodes
        :type nodes: list of Node

        :param kwargs Options (overrides defaults)
        :type kwargs: dict
        """
        self.nodes = list(nodes)
