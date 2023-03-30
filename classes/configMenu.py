from tkinter import Tk, Label, Frame, Entry
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
        frame.pack()
        # Title
        Frame(frame, height=1, width=200).grid(column=0, row=0)
        Label(frame, text="Object " + str(len(self.frames)+1), font=("Calibri 12")).grid(column=1, row=0)
        # Mass
        leftFrame = Frame(frame)
        leftFrame.grid(column=0, row=1)
        Label(leftFrame, text="Mass ", font=("Calibri 11")).grid(column=0, row=0)
        Entry(leftFrame, font=("Calibri 11")).grid(column=1, row=0)
        # Pos
        Label(leftFrame, text="Position x", font=("Calibri 11")).grid(column=0, row=1)
        Entry(leftFrame, font=("Calibri 11")).grid(column=1, row=1)
        Label(leftFrame, text="Position y", font=("Calibri 11")).grid(column=0, row=2)
        Entry(leftFrame, font=("Calibri 11")).grid(column=1, row=2)
        # Velocity 
        rightFrame = Frame(frame)
        rightFrame.grid(column=2, row=1)
        Label(rightFrame, text="Position x", font=("Calibri 11")).grid(column=0, row=0)
        Entry(rightFrame, font=("Calibri 11")).grid(column=1, row=0)
        Label(rightFrame, text="Position y", font=("Calibri 11")).grid(column=0, row=1)
        Entry(rightFrame, font=("Calibri 11")).grid(column=1, row=1)
        # Colour
        Label(rightFrame, text="Colour R", font=("Calibri 11")).grid(column=0, row=2)
        Entry(rightFrame, font=("Calibri 11"), width=3).grid(column=1, row=2, sticky="W")
        Label(rightFrame, text="Colour G", font=("Calibri 11")).grid(column=0, row=3)
        Entry(rightFrame, font=("Calibri 11"), width=3).grid(column=1, row=3, sticky="W")
        Label(rightFrame, text="Colour B", font=("Calibri 11")).grid(column=0, row=4)
        Entry(rightFrame, font=("Calibri 11"), width=3).grid(column=1, row=4, sticky="W")

        return frame

men = Menu()
men.open()