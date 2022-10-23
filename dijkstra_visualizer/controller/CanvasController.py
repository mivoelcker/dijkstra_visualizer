import tkinter as tk
from tkinter import simpledialog
from typing import List, Union

from model.DijkstraAlgorithm import DijkstraAlgorithm
from model.Node import Node
from view.GraphCanvas import GraphCanvas
from view.InfoLabel import InfoLabel


class CanvasController:
    graph_canvas: GraphCanvas
    info_label: InfoLabel
    nodes: List[Node]
    active_node: Union[Node, None] = None
    name_counter: int
    dijkstra_algorithm: Union[DijkstraAlgorithm, None] = None


    def __init__(self, graph_canvas: GraphCanvas, info_label: InfoLabel):
        """
        Controls the canvas and handle the input logic.
        Differentiates between an edit mode and the visualization mode.

        :param graph_canvas: The main canvas
        :param info_label: A label to show further infos.
        """
        self.graph_canvas = graph_canvas
        self.info_label = info_label
        self.nodes = []
        self.name_counter = 0

        self.graph_canvas.bind("<Button-1>", self.on_left_click)
        self.graph_canvas.bind("<Button-3>", self.on_right_click)
        self.graph_canvas.bind("<Button-2>", self.on_middle_click)


    def get_node_on_position(self, x: int, y: int) -> Union[Node, None]:
        """
        Searches for a node on this position.
        If multiple nodes overlap the last one added will be returned.

        :param x: The number of pixel in x-axis (left to right)
        :param y: The number of pixel in y-axis (top to bottom)
        :return: The found node or none
        """
        for node in reversed(self.nodes):
            if node.is_position_in_node(x, y):
                return node
        return None


    def add_node(self, x: int, y: int, name: str = None) -> Node:
        """
        Creates a nodes and adds it to the node list.

        :param x: The number of pixel in x-axis (left to right)
        :param y: The number of pixel in y-axis (top to bottom)
        :param name: The node's name
        :return: And instance of Node
        """
        if not name:
            self.name_counter += 1
            name = str(self.name_counter)

        node = Node(name, x, y)
        self.nodes.append(node)
        return node


    def delete_node(self, node: Node):
        """
        Deletes a node and all its connections.

        :param node: The node to delete
        """
        for neighbour in node.neighbours.copy():
            node.delete_neighbour(neighbour)
        if node is self.active_node:
            self.active_node = None
        self.nodes.remove(node)


    def add_connection(self, start_node: Node, end_node: Node, weight: int = None):
        """
        Adds a connections between to nodes.
        The order of the start and end node does not matter due to the undirected graph.

        :param start_node: First node
        :param end_node: Second node
        :param weight: The connections weight/length
        """
        if weight is None:
            weight = simpledialog.askfloat(
                "Weight",
                f"Input weight for connection between node '{start_node.name}' and node '{end_node.name}'.:",
                parent=self.graph_canvas,
                minvalue=0)

        if weight is not None:
            start_node.add_neighbour(end_node, weight)


    def redraw_canvas(self, nodes: List[Node] = None, active_node: Node = None):
        """
        Redraws the whole canvas.

        :param nodes: A list of node, default are all nodes.
        :param active_node: The currently selected node to emphasize
        """
        nodes = nodes if nodes else self.nodes
        active_node = active_node if active_node else self.active_node
        self.graph_canvas.redraw_graph(nodes, active_node)


    def clear(self):
        """
        Clears all nodes and the canvas.
        """
        self.nodes = []
        self.active_node = None
        self.name_counter = 0
        self.redraw_canvas()


    def on_left_click(self, event: tk.Event):
        """
        Handles input of the left mouse button.
        Depending on the current mode it adds new nodes and connections or shows the shortest path.

        :param event: The input event
        """
        node_unser_mouse = self.get_node_on_position(event.x, event.y)

        if self.dijkstra_algorithm:
            self.draw_shortest_path(node_unser_mouse)
            return

        if not node_unser_mouse:
            node_unser_mouse = self.add_node(event.x, event.y)
            if self.active_node:
                self.add_connection(self.active_node, node_unser_mouse)
            self.active_node = node_unser_mouse

        elif self.active_node and node_unser_mouse is not self.active_node:
            self.add_connection(self.active_node, node_unser_mouse)

        self.redraw_canvas()


    def on_right_click(self, event: tk.Event):
        """
        Handles input of the right mouse button.
        In edit mode it marks the selected node as active.

        :param event: The input event
        """
        if self.dijkstra_algorithm:
            return

        node_unser_mouse = self.get_node_on_position(event.x, event.y)
        if not node_unser_mouse:
            return

        if self.active_node is node_unser_mouse:
            self.active_node = None
        else:
            self.active_node = node_unser_mouse
        self.redraw_canvas()


    def on_middle_click(self, event: tk.Event):
        """
        Handles input of the middle mouse button.
        In edit mode it deletes the selected node.

        :param event: The input event
        """
        if self.dijkstra_algorithm:
            return

        node_unser_mouse = self.get_node_on_position(event.x, event.y)
        if not node_unser_mouse:
            return

        self.delete_node(node_unser_mouse)
        self.redraw_canvas()


    def start_dijkstra(self) -> bool:
        """
        Initializes the Dijkstra algorithm and switches to visualisation mode.

        :return: False if missing start node, else True
        """
        if not self.active_node:
            return False
        self.dijkstra_algorithm = DijkstraAlgorithm(self.nodes, self.active_node)
        self.next_dijkstra()
        self.info_label.set_text(self.info_label.dijkstra_info)
        return True


    def next_dijkstra(self) -> bool:
        """
        Shows the next step of the Dijkstra algorithm.

        :return: False if no more steps else True
        """
        try:
            next(self.dijkstra_algorithm)
            self.draw_dijkstra()
            return True
        except StopIteration:
            self.info_label.set_text(self.info_label.dijkstra_ended_info)
            return False


    def skip_dijkstra(self):
        """
        Skips all steps of the Dijkstra algorithm and shows the finished algorithm.
        """
        while self.dijkstra_algorithm:
            try:
                next(self.dijkstra_algorithm)
            except StopIteration:
                self.draw_dijkstra()
                self.info_label.set_text(self.info_label.dijkstra_ended_info)
                break


    def reset_dijkstra(self):
        """
        Switches back to edit mode and resets all nodes and the canvas.
        """
        if self.dijkstra_algorithm:
            self.dijkstra_algorithm.reset()
            self.dijkstra_algorithm = None
        self.redraw_canvas()
        self.info_label.set_text(self.info_label.base_info)


    def draw_dijkstra(self):
        """
        Redraws the whole canvas and draws the current dijkstra step.
        """
        self.redraw_canvas(self.dijkstra_algorithm.nodes)
        if self.dijkstra_algorithm.current_node:
            outline_color = "red" if self.dijkstra_algorithm.current_node is self.active_node else None
            self.graph_canvas.draw_node(self.dijkstra_algorithm.current_node, outline_color, "green")

            if self.dijkstra_algorithm.current_neighbour:
                self.graph_canvas.draw_node(self.dijkstra_algorithm.current_neighbour, "chartreuse")
                self.graph_canvas.draw_connection(self.dijkstra_algorithm.current_node, self.dijkstra_algorithm.current_neighbour, color="chartreuse")


    def draw_shortest_path(self, target_node: Node):
        """
        Redraws the current dijkstra step and draws the calculated shortest path to the target path.

        :param target_node: The end node of path
        """
        self.draw_dijkstra()
        if not target_node:
            return

        start_node = target_node
        end_node = target_node.predecessor
        while end_node:
            self.graph_canvas.draw_connection(start_node, end_node, color="red")
            start_node = end_node
            end_node = end_node.predecessor

