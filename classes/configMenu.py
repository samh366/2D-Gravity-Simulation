from tkinter import Tk, Label, Frame, Entry, StringVar, OptionMenu, Button, END, messagebox
from tkinter import ttk

from classes.pygameWindow import Window
from classes.simulation import Simulation
from classes.object import Object

TIMESTEP = 24 * 3600 // 1.5

class Menu:
    def __init__(self):
        """A menu that lets you select simulation properties."""
        self.win = Tk()
        self.frames = []
        self._object_count = 0

        # Store scales for the values
        self._scales = {
            "m":1,
            "km":1000,
            "AU":149.6e6 * 1000,
            "m/s":1,
            "km/s":1000,
            "AU/s":149.6e6 * 1000,
            "g":0.001,
            "kg":1,
            "Moons":7.346e22,
            "Earths":5.9722e24,
            "Jupiters":1_898.13e24,
            "Suns":	1_988_500e24,
            "10xSun": 1_988_500e25,
            "100xSun": 1_988_500e26
        }

    def open(self):
        self.win.geometry("600x550")
        self.win.title("Simulation Config")
        self.win.resizable(width=False, height=True)

        Label(self.win, text="Simulation Config", font=("Calibri 20")).pack(pady=15)
        # Run simulation button
        Button(self.win, font=("Calibri 11"), bg="#19d42f", activebackground="#4fe861", text="Run", command=self.run).pack()


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
        Label(rightFrame, text="Velocity x", font=("Calibri 11")).grid(column=0, row=0)
        frameData["vel"].append(Entry(rightFrame, font=("Calibri 11"), width=15))
        frameData["vel"][-1].grid(column=1, row=0, sticky="W")
        Label(rightFrame, text="Velocity y", font=("Calibri 11")).grid(column=0, row=1)
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
        OptionMenu(leftFrame, massVar, "g", "kg", "Moons", "Earths", "Jupiters", "Suns", "10xSun", "100xSun").grid(column=2, row=0, sticky="W")
        frameData["mass"].append(massVar)
        # Pos
        posVarX = StringVar(self.win)
        posVarY = StringVar(self.win)
        posVarX.set("km")
        posVarY.set("km")
        OptionMenu(leftFrame, posVarX, "m", "km", "AU").grid(column=2, row=1, sticky="W")
        OptionMenu(leftFrame, posVarY, "m", "km", "AU").grid(column=2, row=2, sticky="W")
        frameData["pos"].append(posVarX)
        frameData["pos"].append(posVarY)
        # Velocity
        velVarX = StringVar(self.win)
        velVarY = StringVar(self.win)
        velVarX.set("km/s")
        velVarY.set("km/s")
        OptionMenu(rightFrame, velVarX, "m/s", "km/s", "AU/s").grid(column=2, row=0, sticky="W")
        OptionMenu(rightFrame, velVarY, "m/s", "km/s", "AU/s").grid(column=2, row=1, sticky="W")
        frameData["vel"].append(velVarX)
        frameData["vel"].append(velVarY)

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

    def export_parameters(self) -> tuple:
        """
        Exports the information contained within the widgets in the below format

        Returns:
        (
            (mass, (posx, posy), (velx, vely), (colR, colG, colB)), ...
        )
        """
        output = []

        for frame in self.frames:
            data = (
                (frame["mass"][0].get(), frame["mass"][1].get()),
                (frame["pos"][0].get(), frame["pos"][1].get()),
                (frame["pos"][2].get(), frame["pos"][3].get()),
                (frame["vel"][0].get(), frame["vel"][1].get()),
                (frame["vel"][2].get(), frame["vel"][3].get()),
                (frame["col"][0].get()),
                (frame["col"][1].get()),
                (frame["col"][2].get()),
                (frame["name"].get())
            )
            
            try:
                output.append(self.translate_parameters(data))
            except ValueError:
                self.handle_input_error(frame["name"].get(), frame["name"], "Input values must be decimals")

        return output

    
    def translate_parameters(self, data) -> tuple[float]:
        """Converts values entered by the user to values suggest by scale boxes"""
        output = ()
        for i, section in enumerate(data):
            if len(section) == 2:
                output.append(
                    float(section[0]) * self._scales[section[1]]
                )
            elif i != 8:
                if int(section[0]) > 255 or int(section[0]) < 0:
                    self.handle_input_error(data[-1][0], "Invalid color value!")
                    return None
                output.append(int(section[0]))
            else:
                output.append(section[0])

        return output

    def handle_input_error(self, name, error):
        """Handles errors found when trying to run the values inputted"""
        messagebox.showerror("Input Error", "Error on '{}'\n{}".format(name, error))

    
    def run(self):
        data = self.export_parameters()
        if data != None:
            self.simulation = Simulation(*(Object(
                mass=i[0],
                pos=(i[1], i[2]),
                velocity=(i[3], i[4]),
                color=(i[5], i[6], i[7])) for i in data), timestep=TIMESTEP)

            self.pygameWindow = Window(screenSize=(800, 800), scale=self.simulation.estimate_scale())
            self.pygameWindow.simulate()



men = Menu()
men.open()