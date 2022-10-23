import json
from pathlib import Path
from tkinter import filedialog

from controller.CanvasController import CanvasController
from view.ButtonFrame import ButtonFrame


class FileController:
    last_directory: Path = Path(__file__).parent.parent.parent / "data/"


    def __init__(self, canvas_controller: CanvasController, button_frame: ButtonFrame):
        """
        Controls the functionality of the file menu.

        :param canvas_controller: The current canvas controller
        :param button_frame: The current button frame
        """
        self.canvas_controller = canvas_controller
        self.button_frame = button_frame


    def open_file(self, file: Path = None):
        """
        Reads a file and loads its config.
        If no file is given a filedialog will be opened.

        :param file: The file to read, if None a filedialog will be opened
        """
        if not file:
            print(self.last_directory)
            file_name = filedialog.askopenfilename(filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), initialdir=self.last_directory)
            if not file_name:
                return
            file = Path(file_name)
            self.last_directory = file

        json_string = file.read_text()
        nodes_dict = json.loads(json_string)

        self.canvas_controller.clear()

        nodes = []
        for node_dict in nodes_dict["nodes"]:
            nodes.append(self.canvas_controller.add_node(node_dict["x"], node_dict["y"], node_dict["name"]))

        # Add connections
        for node, node_dict in zip(nodes, nodes_dict["nodes"]):
            for neighbour_dict, weight in zip(node_dict["neighbours"], node_dict["weights"]):
                x, y = neighbour_dict["x"], neighbour_dict["y"]
                neighbour = next((n for n in nodes if n.x == x and n.y == y))
                self.canvas_controller.add_connection(node, neighbour, weight)

        self.canvas_controller.name_counter = max((int(n.name) for n in nodes if n.name.isdigit())) + 1
        self.canvas_controller.reset_dijkstra()
        self.button_frame.edit_button_frame.tkraise()


    def save_file(self, file: Path = None):
        """
        Saves the current graph as JSON file.
        If no file is given a filedialog will be opened.

        :param file: The file to write, if None a filedialog will be opened
        """
        node_dicts = [n.to_dict() for n in self.canvas_controller.nodes]
        json_string = json.dumps({"nodes": node_dicts})
        if not file:
            file_name = filedialog.asksaveasfilename(filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), initialdir=self.last_directory)
            if not file_name:
                return
            file = Path(file_name)
            self.last_directory = file

        file.write_text(json_string)




