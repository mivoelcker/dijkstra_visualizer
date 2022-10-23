from typing import List, Tuple, Union, Iterator

from model.Node import Node


class DijkstraAlgorithm:
    current_node: Union[Node, None] = None
    current_neighbour: Union[Node, None] = None
    __generator: Iterator[Tuple[Union[Node, None], Union[Node, None]]]


    def __init__(self, nodes: List[Node], start_node: Node):
        """
        Implements the Dijkstra algorithm and servers as iterator.

        :param nodes: All current nodes
        :param start_node: The start node
        """
        self.nodes = nodes
        self.start_node = start_node
        self.__generator = self.__dijkstra_algorithm()


    def reset(self):
        """
        Resets all nodes' Dijkstra specific attributs
        """
        for node in self.nodes:
            node.reset_dijkstra_attributes()
        self.current_node = None
        self.current_neighbour = None


    def __initialize_nodes(self) -> List[Node]:
        """
        Initializes all nodes for the algorithm.

        :return: A (shallow) copy of the current list
        """
        for node in self.nodes:
            node.distance = float('inf')
            node.predecessor = None
            node.checked = False
        self.start_node.distance = 0
        return self.nodes.copy()


    def __dijkstra_algorithm(self) -> Iterator[Tuple[Union[Node, None], Union[Node, None]]]:
        """
        The Dijkstra algorithm implemented as generator.
        Yields every step the currently active node and the currently checked neighbour.

        :return: A generator
        """
        unchecked_nodes = self.__initialize_nodes()

        while len(unchecked_nodes):
            current_node = min(unchecked_nodes, key=lambda n: n.distance)
            yield current_node, None

            # If the smallest distance is inf, the graph is  not connected
            if current_node.distance == float('inf'):
                for node in unchecked_nodes:
                    node.checked = True
                unchecked_nodes.clear()
                yield None, None
                break

            for neighbour, weight in zip(current_node.neighbours, current_node.weights):
                if not neighbour.checked:
                    yield current_node, neighbour
                    new_distance = current_node.distance + weight
                    if new_distance < neighbour.distance:
                        neighbour.distance = new_distance
                        neighbour.predecessor = current_node
                        yield current_node, neighbour

            current_node.checked = True
            unchecked_nodes.remove(current_node)

            yield None, None


    def next(self) -> Tuple[List[Node], Union[Node, None], Union[Node, None]]:
        """
        Loads and returns the next algorithm's step.
        :return: A tuple of a list with all nodes, the currently active node and the currently checked neighbour
        """
        self.current_node, self.current_neighbour = next(self.__generator)
        return self.nodes, self.current_node, self.current_neighbour


    def __iter__(self):
        return self


    def __next__(self):
        return self.next()
