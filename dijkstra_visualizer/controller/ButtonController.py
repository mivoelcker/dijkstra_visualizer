from tkinter import messagebox

from controller.CanvasController import CanvasController
from view.ButtonFrame import ButtonFrame


class ButtonController:
    def __init__(self, button_frame: ButtonFrame, canvas_controller: CanvasController):
        """
        Controller for the application's buttons.

        :param button_frame: Reference to the button frame to bind the buttons.
        :param canvas_controller: Reference to the canvas controller to start correct methods.
        """
        self.canvas_controller = canvas_controller
        self.button_frame = button_frame

        # Bind correct methods to buttons
        button_frame.button_clear.config(command=self.button_clear_on_click)
        button_frame.button_start.config(command=self.button_start_on_click)
        button_frame.button_reset.config(command=self.button_reset_on_click)
        button_frame.button_next.config(command=self.button_next_on_click)
        button_frame.button_skip.config(command=self.button_skip_on_click)


    def button_clear_on_click(self):
        """
        Clears the canvas.
        """
        self.canvas_controller.clear()


    def button_start_on_click(self):
        """
        Starts the Dijkstra algorithm and changes to buttons.
        """
        if self.canvas_controller.start_dijkstra():
            self.button_frame.dijkstra_button_frame.tkraise()
        else:
            messagebox.showinfo("No node selected", "Use a right click to select a node as start.")


    def button_reset_on_click(self):
        """
        Resets to canvas into edit mode.
        """
        self.canvas_controller.reset_dijkstra()
        self.button_frame.button_next.config(state='normal')
        self.button_frame.button_skip.config(state='normal')
        self.button_frame.edit_button_frame.tkraise()

    def button_next_on_click(self):
        """
        Shows the next step of the Dijkstra algorithm.
        """
        if not self.canvas_controller.next_dijkstra():
            self.button_frame.button_next.config(state='disabled')
            self.button_frame.button_skip.config(state='disabled')


    def button_skip_on_click(self):
        """
        Skips all steps and finishes the Dijkstra algorithm.
        """
        self.canvas_controller.skip_dijkstra()
        self.button_frame.button_next.config(state='disabled')
        self.button_frame.button_skip.config(state='disabled')