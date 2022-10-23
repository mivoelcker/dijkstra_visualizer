import tkinter as tk

from controller.FileController import FileController


class MenuBar(tk.Menu):
    def __init__(self, root: tk.Misc, file_controller: FileController):
        """
        A simple menu bar with open and save functionality.

        :param root: The menu's parent
        :param file_controller: The current file controller
        """
        super().__init__(root)
        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="Open file", command=file_controller.open_file)
        self.file_menu.add_command(label="Save", command=file_controller.save_file)
        self.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)
