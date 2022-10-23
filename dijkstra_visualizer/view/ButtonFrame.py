import tkinter as tk
from tkinter import ttk


class ButtonFrame(ttk.Frame):
    def __init__(self, root: tk.Misc):
        """
        A frame containing all buttons of the application.
        Divided in two button groups.

        :param root: The frame's parent
        """
        super().__init__(root)
        self.columnconfigure(0, weight=1)

        # Edit-button group
        self.edit_button_frame = ttk.Frame(self)
        self.edit_button_frame.grid(row=0, sticky='EW')
        self.edit_button_frame.columnconfigure(0, weight=1)
        self.edit_button_frame.columnconfigure(1, weight=1)

        self.button_clear = ttk.Button(self.edit_button_frame, text="Clear")
        self.button_clear.grid(column=0, row=0, sticky='EW')
        self.button_start = ttk.Button(self.edit_button_frame, text="Start Dijkstra")
        self.button_start.grid(column=1, row=0, sticky='EW')

        # Dijkstra-button group
        self.dijkstra_button_frame = ttk.Frame(self)
        self.dijkstra_button_frame.grid(row=0, column=0, sticky='EW')
        self.dijkstra_button_frame.columnconfigure(0, weight=1)
        self.dijkstra_button_frame.columnconfigure(1, weight=1)
        self.dijkstra_button_frame.columnconfigure(2, weight=1)

        self.button_reset = ttk.Button(self.dijkstra_button_frame, text="Reset")
        self.button_reset.grid(column=0, row=1, sticky='EW')
        self.button_skip = ttk.Button(self.dijkstra_button_frame, text="Skip to End")
        self.button_skip.grid(column=1, row=1, sticky='EW')
        self.button_next = ttk.Button(self.dijkstra_button_frame, text="Next Step")
        self.button_next.grid(column=2, row=1, sticky='EW')

        self.edit_button_frame.tkraise()

