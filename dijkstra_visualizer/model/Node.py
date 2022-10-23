from __future__ import annotations

import math
from typing import List, Union, Dict


class Node:
    radius: int = 25
    name: str
    x: int
    y: int
    neighbours: List[Node]
    weights: List[float]
    distance: Union[float, None] = None
    predecessor: Union[Node, None] = None
    checked: bool = False


    def __init__(self, name: str, x: int, y: int):
        """
        Representing a graph's node.

        :param name: The node's name
        :param x: The number of pixel in x-axis (left to right)
        :param y: The number of pixel in y-axis (top to bottom)
        """
        self.name = name
        self.neighbours = []
        self.weights = []
        self.x = x
        self.y = y


    def is_position_in_node(self, x: int, y: int) -> bool:
        """
        Checks if the given position is inside this node.

        :param x: The number of pixel in x-axis (left to right)
        :param y: The number of pixel in y-axis (top to bottom)
        :return: True if postion is inside the nodes circle else false
        """
        dx = abs(x - self.x)
        if dx > self.radius:
            return False

        dy = math.sqrt(self.radius ** 2 - dx ** 2)
        return (self.y - dy) <= y <= (self.y + dy)


    def add_neighbour(self, node: Node, weight: int,):
        """
        Adds the given node as neighbour and vice versa.

        :param node: The neighbour node
        :param weight: The weight of the connection
        """
        self.__add_neighbour(node, weight)
        node.__add_neighbour(self, weight)


    def delete_neighbour(self, node: Node):
        """
        Deletes a connection between this and the given node and vice versa.

        :param node: The neighbour node
        """
        self.__delete_neighbour(node)
        node.__delete_neighbour(self)


    def reset_dijkstra_attributes(self):
        """
        Resets all attributes related to the Dijkstra algorithm.
        """
        self.distance = None
        self.predecessor = None
        self.checked = False


    def __add_neighbour(self, node: Node, weight: int):
        """
        Adds the given node as neighbour.

        :param node: The neighbour node
        :param weight: The weight of the connection
        """
        if weight <= 0:
            self.__delete_neighbour(node)
            return

        if node in self.neighbours:
            index = self.neighbours.index(node)
            self.weights[index] = weight
        else:
            self.neighbours.append(node)
            self.weights.append(weight)


    def __delete_neighbour(self, node: Node):
        """
        Deletes a connection between this and the given node.

        :param node: The neighbour node
        """
        if node in self.neighbours:
            index = self.neighbours.index(node)
            self.neighbours.pop(index)
            self.weights.pop(index)


    def to_dict(self) -> Dict:
        """
        Returns the important attributes as dictionary.
        Ignores the Dijkstra related attributs.

        :return: A dictionary of all important attributes
        """
        return {
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "neighbours": [{"x": n.x, "y": n.y, "name": n.name} for n in self.neighbours],
            "weights": self.weights
        }
