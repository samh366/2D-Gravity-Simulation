from tkinter import Tk, Label, Frame, Entry, StringVar, OptionMenu, Button, END
from tkinter import ttk

class Menu:
    def __init__(self):
        """A menu that lets you select simulation properties."""
        self.win = Tk()
        self.frames = []
        self._object_count = 0

    def open(self):
        self.win.geometry("600x550")
        self.win.title("Simulation Config")
        self.win.resizable(width=False, height=True)

        Label(self.win, text="Simulation Config", font=("Calibri 20")).pack(pady=15)
        self.objectFrame = Frame(self.win)
        self.objectFrame.pack()
        # Forces the object frame to resize when nothing is in it
        Frame(self.objectFrame, width=1, height=1).pack()
        self.addObjectButton = Button(self.win, font=("Calibri 11"), bg="#119ad9", activebackground="#42b5eb", text="+ Add Object", command=self.add_frame)
        self.addObjectButton.pack()

        self.win.mainloop()

    def add_frame(self):
        """Adds a frame and all its appropriate elements"""
        frame = Frame(self.objectFrame, highlightbackground="black", highlightthickness=1)
        frame.pack()
        frameData = {"frame":frame, "mass":[], "pos":[], "vel":[], "col":[]}
        frameData["id"] = len(self.frames)
        self._object_count += 1
        # Title
        frameData["name"] = Entry(frame, font=("Calibri 12"), width=15)
        frameData["name"].grid(column=0, row=0, columnspan=3)
        frameData["name"].insert(0, "Object " + str(self._object_count))
        # Line
        Frame(frame, height=1, width=400, highlightbackground="black", highlightthickness=1).grid(column=0, row=1, columnspan=3, pady=5)
        # Mass
        leftFrame = Frame(frame)
        leftFrame.grid(column=0, row=2)
        Label(leftFrame, text="Mass ", font=("Calibri 11")).grid(column=0, row=0)
        frameData["mass"].append(Entry(leftFrame, font=("Calibri 11"), width=15))
        frameData["mass"][-1].grid(column=1, row=0, sticky="W")
        # Pos
        Label(leftFrame, text="Position x", font=("Calibri 11")).grid(column=0, row=1)
        frameData["pos"].append(Entry(leftFrame, font=("Calibri 11"), width=15))
        frameData["pos"][-1].grid(column=1, row=1, sticky="W")
        Label(leftFrame, text="Position y", font=("Calibri 11")).grid(column=0, row=2)
        frameData["pos"].append(Entry(leftFrame, font=("Calibri 11"), width=15))
        frameData["pos"][-1].grid(column=1, row=2, sticky="W")
        # Velocity 
        rightFrame = Frame(frame)
        rightFrame.grid(column=2, row=2)
        Label(rightFrame, text="Position x", font=("Calibri 11")).grid(column=0, row=0)
        frameData["vel"].append(Entry(rightFrame, font=("Calibri 11"), width=15))
        frameData["vel"][-1].grid(column=1, row=0, sticky="W")
        Label(rightFrame, text="Position y", font=("Calibri 11")).grid(column=0, row=1)
        frameData["vel"].append(Entry(rightFrame, font=("Calibri 11"), width=15))
        frameData["vel"][-1].grid(column=1, row=1, sticky="W")
        # Colour
        Label(rightFrame, text="Colour R", font=("Calibri 11")).grid(column=0, row=2)
        frameData["col"].append(Entry(rightFrame, font=("Calibri 11"), width=3))
        frameData["col"][-1].grid(column=1, row=2, sticky="W")
        Label(rightFrame, text="Colour G", font=("Calibri 11")).grid(column=0, row=3)
        frameData["col"].append(Entry(rightFrame, font=("Calibri 11"), width=3))
        frameData["col"][-1].grid(column=1, row=3, sticky="W")
        Label(rightFrame, text="Colour B", font=("Calibri 11")).grid(column=0, row=4)
        frameData["col"].append(Entry(rightFrame, font=("Calibri 11"), width=3))
        frameData["col"][-1].grid(column=1, row=4, sticky="W")

        # Dropdown boxes
        # Mass
        massVar = StringVar(self.win)
        massVar.set("kg")
        frameData["mass"].append(OptionMenu(leftFrame, massVar, "g", "kg", "Earths", "Jupiters", "Suns", "10xSun", "100xSun"))
        frameData["mass"][-1].grid(column=2, row=0, sticky="W")
        # Pos
        posVar = StringVar(self.win)
        posVar.set("km")
        frameData["pos"].append(OptionMenu(leftFrame, posVar, "m", "km", "AU"))
        frameData["pos"][-1].grid(column=2, row=1, sticky="W")
        frameData["pos"].append(OptionMenu(leftFrame, posVar, "m", "km", "AU"))
        frameData["pos"][-1].grid(column=2, row=2, sticky="W")
        # Velocity
        velVar = StringVar(self.win)
        velVar.set("km/s")
        frameData["vel"].append(OptionMenu(rightFrame, velVar, "m/s", "km/s", "AU/s"))
        frameData["vel"][-1].grid(column=2, row=0, sticky="W")
        frameData["vel"].append(OptionMenu(rightFrame, velVar, "m/s", "km/s", "AU/s"))
        frameData["vel"][-1].grid(column=2, row=1, sticky="W")

        # Remove button
        frameData["remove"] = Button(
                                leftFrame, font=("Calibri 11"),
                                bg="#eb4034", activebackground="#f06e65",
                                text="Remove", highlightcolor="#f06e65",
                                command=lambda: self.remove_frame_by_index(frameData["id"]))
        frameData["remove"].grid(column=0, row=3, columnspan=3)

        self.frames.append(frameData)
    
    # Should only be called on the topmost frame
    def remove_frame_by_index(self, index):
        # Handles any child frames that contain their own index
        self.remove_frame(self.frames[index]["frame"])
        del self.frames[index]
        self.reorder_objects()

    def remove_frame(self, frame):
        # Destroy all children
        for child in frame.winfo_children():
            if isinstance(child, Frame):
                self.remove_frame(child)
            child.destroy()
            del child
        frame.destroy()

    def reorder_objects(self):
        for index, val in enumerate(self.frames):
            # val["name"].delete(0, END) 
            # val["name"].insert(0, "Object " + str(index+1))
            val["id"] = index


men = Menu()
men.open()