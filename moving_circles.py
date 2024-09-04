"""
File: moving_circles.py 
Author: Rodolfo Lopez and Justin de Sousa
Date: 3/14/2020
Description: Program that gets two circle locations from the
user, then draws a line between them, and 
displays the distance between them midway along
the line.  The user can drag either circle around,
and the distance is kept updated.
"""

import math
import tkinter as tk
from enum import IntEnum


class MovingCircles:
    """Initializes the Circle Objects"""

    def __init__(self):
        # Create Window
        self.window = tk.Tk()
        self.window.title("Moving Circles")

        # Initialize Variables
        self.circle_1 = None
        self.circle_2 = None
        self.line = None
        self.size = 400
        self.radius = 20
        self.color = "red"
        self.distance = None
        self.distance_text = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.state = CanvasState.NOCIRCLE
        self.delta_x = None
        self.delta_y = None

        # Create Canvas
        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size)
        self.canvas.grid(row=1, column=1)

        # Bind Mouse to Handler Methods
        self.canvas.bind("<Button-1>", self.mouse_handler)

        # Create Button Frame
        self.button_frame = tk.Frame(self.window, width=self.size, height=50)
        self.button_frame.grid(row=2, column=1)

        # Put Clear Button in Button Frame
        self.clear_button = tk.Button(
            self.button_frame, text="Clear", command=self.clear
        )
        self.clear_button.grid(row=1, column=1)

        # Put Quit Button in Button Frame
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=1, column=2)

        # Window Mainloop
        self.window.mainloop()

    def mouse_handler(self, event):
        """Function that creates the circles and line using a state system to keep track. The states update each time the user clicks.
        The first state creates a circle where the user clicks. The second state creates another cicle where the user clicks as
        well as a line with the distance calculated at the center of the line. It then binds the coresponding handler to each circle
        """
        if self.state == CanvasState.NOCIRCLE:
            self.x1 = event.x
            self.y1 = event.y
            self.circle_1 = self.canvas.create_oval(
                self.x1 - self.radius,
                self.y1 - self.radius,
                self.x1 + self.radius,
                self.y1 + self.radius,
                fill="red",
            )
            self.state = CanvasState.CIRCLE
        elif self.state == CanvasState.CIRCLE:
            self.x2 = event.x
            self.y2 = event.y
            self.circle_2 = self.canvas.create_oval(
                self.x2 - self.radius,
                self.y2 - self.radius,
                self.x2 + self.radius,
                self.y2 + self.radius,
                fill="red",
            )
            self.line = self.canvas.create_line(
                self.x1, self.y1, self.x2, self.y2, fill="red"
            )
            self.distance = math.sqrt(
                (self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2
            )
            self.distance = format(self.distance, ".2f")
            self.center_x = (self.x1 + self.x2) / 2
            self.center_y = (self.y1 + self.y2) / 2
            self.distance_text = self.canvas.create_text(
                self.center_x, self.center_y, text=self.distance
            )
            self.state = CanvasState.CIRCLES
        else:
            self.canvas.tag_bind(self.circle_1, "<B1-Motion>", self.motion_handler_1)
            self.canvas.tag_bind(self.circle_2, "<B1-Motion>", self.motion_handler_2)

    def motion_handler_1(self, event):
        """This handler is bound to the first cicle and moves the circle when it is clicked wherever the user drags. It also deletes and reprints the line"""
        self.canvas.delete(self.distance_text)
        self.canvas.delete(self.line)
        self.delta_x = event.x - self.x1
        self.delta_y = event.y - self.y1
        self.canvas.move(self.circle_1, self.delta_x, self.delta_y)
        self.x1 = event.x
        self.y1 = event.y
        self.line = self.canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill="red"
        )
        self.distance = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.distance = format(self.distance, ".2f")
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2
        self.distance_text = self.canvas.create_text(
            self.center_x, self.center_y, text=self.distance
        )

    def motion_handler_2(self, event):
        """This function does the same as the first but with the second circle"""
        self.canvas.delete(self.line)
        self.canvas.delete(self.distance_text)
        self.delta_x = event.x - self.x2
        self.delta_y = event.y - self.y2
        self.canvas.move(self.circle_2, self.delta_x, self.delta_y)
        self.x2 = event.x
        self.y2 = event.y
        self.line = self.canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill="red"
        )
        self.distance = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.distance = format(self.distance, ".2f")
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2
        self.distance_text = self.canvas.create_text(
            self.center_x, self.center_y, text=self.distance
        )

    def clear(self):
        """Resets canvas to original state"""
        self.canvas.delete("all")
        self.state = CanvasState.NOCIRCLE

    def quit(self):
        """Terminates the program"""
        self.window.destroy()


class CanvasState(IntEnum):
    """
    Use IntEnum for Canvas States
    """

    NOCIRCLE = 0
    CIRCLE = 1
    CIRCLES = 2


if __name__ == "__main__":
    # Create GUI
    MovingCircles()
