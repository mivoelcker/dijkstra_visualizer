import math
import tkinter as tk
from typing import List

from model.Node import Node


class GraphCanvas(tk.Canvas):
    def __init__(self, root: tk.Misc, width: int = None, height: int = None):
        """
        The main canvas displays all nodes.
        Servers methods to draw needed figures.

        :param root: The canvas parent
        :param width: The width of the canvas
        :param height: The height of the canvas
        """
        super().__init__(root, width=width, height=height, bg="white")


    def redraw_graph(self, nodes: List[Node], active_node: Node = None):
        """
        Clears the canvas and redraws all given nodes and connections.

        :param nodes: All nodes to draw on canvas
        :param active_node: The currently selected node will be highlighted
        """
        self.delete("all")

        finished_nodes = []  # Save finished node to prevent connections from being drawn multiple times
        for node in nodes:
            outline_color = "red" if node is active_node else None
            fill_color = "dark sea green" if node.checked else None
            self.draw_node(node, outline_color, fill_color)

            for neighbour, weight in zip(node.neighbours, node.weights):
                if neighbour not in finished_nodes:
                    self.draw_connection(node, neighbour, weight)

            finished_nodes.append(node)


    def draw_node(self, node: Node, outline_color: str = None, fill_color: str = None):
        """
        Draws a single node on the canvas.

        :param node: The node to draw
        :param outline_color: Color of the node's outline
        :param fill_color: Color of the node's background
        """
        outline_color = outline_color if outline_color else "black"
        fill_color = fill_color if outline_color else "black"

        self.create_oval(
            (node.x - node.radius, node.y - node.radius),
            (node.x + node.radius, node.y + node.radius),
            width=2,
            outline=outline_color,
            fill=fill_color
        )
        text = node.name if node.distance is None else f"{node.name}\n<{node.distance}>"
        self.create_text(node.x, node.y, text=text, justify='center')


    def draw_connection(self, start_node: Node, end_node: Node, weight: float = 0.0, color: str = None):
        """
        Draws a single connection.
        Order of start and end node is unimportant.

        :param start_node: First node
        :param end_node: Second node
        :param weight: Weight of the connection
        :param color: The line's color
        """
        color = color if color else "black"

        dx = end_node.x - start_node.x
        dy = end_node.y - start_node.y
        phi = math.atan(dy / dx) if dx != 0 else math.copysign(math.pi / 2, dy)
        sign = math.copysign(1, dx)

        start_x = start_node.x + sign * start_node.radius * math.cos(phi)
        start_y = start_node.y + sign * start_node.radius * math.sin(phi)
        end_x = end_node.x - sign * end_node.radius * math.cos(phi)
        end_y = end_node.y - sign * end_node.radius * math.sin(phi)
        self.create_line((start_x, start_y), (end_x, end_y), width=2, fill=color)

        if weight:
            text_height = 7
            mid_x = (start_x + end_x) / 2 + math.sin(phi) * text_height
            mid_y = (start_y + end_y) / 2 - math.cos(phi) * text_height
            self.create_text((mid_x, mid_y), text=str(weight), angle=phi * -180 / math.pi)



