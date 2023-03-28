from tkinter import Tk, Label, Frame
from tkinter import ttk

class Menu:
    def __init__(self):
        """A menu that lets you select simulation properties."""
        self.win = Tk()
        self.frames = []

    def open(self):
        self.win.geometry("600x550")
        self.win.title("Simulation Config")

        Label(self.win, text="Simulation Config", font=("Calibri 20")).pack(pady=15)
        self.frames.append(self.addFrame())

        self.win.mainloop()

    def addFrame(self) -> Frame:
        """Adds a frame and all its appropriate elements"""
        frame = Frame(self.win, height=100, width=550, borderwidth=2, relief="sunken")
        # Title
        Label(frame, text="Object " + str(len(self.frames)+1), font=("Calibri 12")).grid(column=0, row=0)

        frame.pack()
        return frame

men = Menu()
men.open()