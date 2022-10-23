import tkinter as tk
from tkinter import ttk


class InfoLabel(ttk.Label):
    base_info = "Use the right mouse button to select a node and press start to run the Dijkstra algorithm. \n" \
                "Use left the mouse button to add more nodes or connections. \n" \
                "Use the middle mouse button to delete nodes or click clear to delete all. \n" \
                "To save and load files use the file menu."

    dijkstra_info = "Click next to show all steps of the Dijkstra algorithm or skip to the end. \n" \
                    "Use left the mouse button to show the shortest path to this node. \n" \
                    "Click reset to switch back to the edit mode."

    dijkstra_ended_info = "The Dijkstra algorithm finished. \n" \
                          "Use left click to select a node and to show the shortest path. \n" \
                          "Click reset to switch back to the edit mode."

    def __init__(self, root: tk.Misc):
        """
        A label for some user info.

        :param root: The label's parent
        """
        super().__init__(root)
        self.set_text(self.base_info)


    def set_text(self, text: str = ""):
        """
        Sets the lable's text.

        :param text: The text to display
        """
        self.config(text=text)
