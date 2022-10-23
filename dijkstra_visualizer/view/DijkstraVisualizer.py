import tkinter as tk
import warnings
from pathlib import Path

from controller.ButtonController import ButtonController
from controller.CanvasController import CanvasController
from controller.FileController import FileController
from view.ButtonFrame import ButtonFrame
from view.GraphCanvas import GraphCanvas
from view.InfoLabel import InfoLabel
from view.MenuBar import MenuBar


class DijkstraVisualizer(tk.Tk):
    CANVAS_WIDTH: int = 1000
    CANVAS_HEIGHT: int = 600
    DEFAULT_FILE: str = "../../data/example-1.json"  # Relative to file position


    def __init__(self):
        """
        A tkinter app for a visualization of the Dijkstra algorithm.
        """
        super().__init__()
        self.title("Dijkstra Visualizer")
        self.resizable(False, False)

        # Info label
        self.info_label = InfoLabel(self)
        self.info_label.grid(row=0, sticky='EW', pady=2, padx=4)

        # Main canvas
        self.graph_canvas = GraphCanvas(self, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.graph_canvas.grid(row=1)
        self.canvas_controller = CanvasController(self.graph_canvas, self.info_label)

        # Button bar
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=2, sticky='EW')
        self.button_controller = ButtonController(self.button_frame, self.canvas_controller)

        # Menu bar
        self.file_controller = FileController(self.canvas_controller, self.button_frame)
        self.menu = MenuBar(self, self.file_controller)
        self.config(menu=self.menu)

        # Load default example if it exists
        default_file = (Path(__file__).parent / Path(self.DEFAULT_FILE)).resolve()
        if default_file.exists():
            self.file_controller.open_file(default_file)
        else:
            warnings.warn(f"Could not find default example ({default_file})!")

