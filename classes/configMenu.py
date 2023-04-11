import json
import os
from tkinter import (Button, Entry, Frame, Label, Menu, OptionMenu, StringVar,
                     Tk, filedialog, messagebox)

import pygame

from classes.object import Object
from classes.pygameWindow import Window
from classes.scrollableFrame import ScrollFrame
from classes.simulation import Simulation


class ConfigMenu:
    def __init__(self, directory):
        """A menu that lets you select simulation properties."""
        self.win = Tk()
        self.frames = []
        self._object_count = 0
        self._directory = directory

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
        self.win.resizable(width=True, height=True)

        self.menu_bar()

        Label(self.win, text="Simulation Config", font=("Calibri 20")).pack(pady=15)
        # Run simulation button
        Button(self.win, font=("Calibri 11"), bg="#19d42f", activebackground="#4fe861", text="Run", command=self.run).pack()

        # Timestep input
        self.timeStepFrame = Frame()
        self.timeStepFrame.pack()
        Label(self.timeStepFrame, text="Time per frame (60fps): ", font=("Calibri 13")).grid(column=0, row=0, sticky="W")
        self.timeStepData = Entry(self.timeStepFrame, font=("Calibri 11"), width=12)
        self.timeStepData.insert(0, "0.5")
        self.timeStepData.grid(column=1, row=0, sticky="W")
        self.timeStepVar = StringVar(self.win)
        self.timeStepVar.set("Days")
        OptionMenu(self.timeStepFrame, self.timeStepVar, "Seconds", "Minutes", "Hours", "Days", "Weeks", "Years", "1000 years", "Mil years").grid(column=2, row=0, sticky="W")

        # Iterations per frame input
        self.iterationsFrame = Frame()
        self.iterationsFrame.pack()
        Label(self.iterationsFrame, text="Iterations per frame: ", font=("Calibri 13")).grid(column=0, row=0, sticky="W")
        self.iterationsData = Entry(self.iterationsFrame, font=("Calibri 11"), width=5)
        self.iterationsData.insert(0, "8")
        self.iterationsData.grid(column=1, row=0, sticky="W")
        

        # Add object button
        self.addObjectButton = Button(self.win, font=("Calibri 11"), bg="#119ad9", activebackground="#42b5eb", text="+ Add Object", command=self.add_frame)
        self.addObjectButton.pack()


        self.objectFrame = ScrollFrame(self.win)
        self.objectFrame.pack(side="top", fill="both", expand=True)


        # Forces the object frame to resize when nothing is in it
        # Frame(self.objectFrame, width=1, height=1).pack()

        self.win.mainloop()

    def menu_bar(self):
        """Code to create the menu bar"""
        self.menubar = Menu(self.win)
        file = Menu(self.menubar, tearoff=False)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Load", command=self.load)
        file.add_command(label="Exit", command=self.win.quit)
        self.menubar.add_cascade(label="File", menu=file)

        self.win.config(menu=self.menubar)

    def get_timestep(self):
        """Gets the data from the timestep inputs"""
        # Scales
        scales = {
            "Seconds" : 1,
            "Minutes" : 60,
            "Hours" : 3600,
            "Days" : 86400,
            "Weeks" : 86400*7,
            "Years" : 86400*7*52,
            "1000 years" : 86400*7*52*1000,
            "Mil years" : 86400*7*52*1_000_000
        }
        output = float(self.timeStepData.get())
        output *= scales[self.timeStepVar.get()]
        return output

    def get_iterations(self):
        return int(self.iterationsData.get())

    def add_frame(self):
        """Adds a frame and all its appropriate elements"""
        frame = Frame(self.objectFrame.viewPort, highlightbackground="black", highlightthickness=1)
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
        if len(self.frames) == 0:
            self.handle_input_error("input", "Cannot run simulation with no objects!")
            return None
        output = []

        for frame in self.frames:
            data = self.getInputFromBoxes(frame)
            
            try:
                translated = self.translate_parameters(data)
                if translated != None:
                    output.append(translated)
                else:
                    return None
            except FileNotFoundError:
                self.handle_input_error(frame["name"].get(), "Invalid data format, use integers for colours\nand decimals for everything else!")
                return None
        
        # Get timestep
        try:
            output.append(self.get_timestep())
        except ValueError:
            self.handle_input_error("Time-step", "Invalid timestep, please enter a decimal/integer number")

        # Get iterations
        try:
            output.append(self.get_iterations())
        except ValueError:
            self.handle_input_error("Iterations", "Invalid number of iterations per frame, must be integer")

        return output

    
    def translate_parameters(self, data) -> tuple[float]:
        """Converts values entered by the user to values suggest by scale boxes"""
        output = []
        for i, section in enumerate(data):
            if isinstance(section, list):
                output.append(
                    float(section[0]) * self._scales[section[1]]
                )
            elif i != 8:
                if int(section) > 255 or int(section) < -1:
                    self.handle_input_error(data[-1][0], "Invalid color value!")
                    return None
                output.append(int(section))
            else:
                output.append(section)

        return output

    def handle_input_error(self, name, error):
        """Handles errors found when trying to run the values inputted"""
        messagebox.showerror("Input Error", "Error on '{}'\n{}".format(name, error))

    
    def run(self):
        data = self.export_parameters()
        if data != None:
            self.simulation = Simulation(
                objects=(
                    Object(
                        mass=i[0],
                        pos=(i[1], i[2]),
                        velocity=(i[3], i[4]),
                        color=(i[5], i[6], i[7]),
                        name=i[8]
                        )
                    for i in data if isinstance(i, list)),
                timestep=data[-2],
                iterations=data[-1])

            pygame.init()
            pygame.font.init()
            self.pygameWindow = Window(screenSize=(800, 800), scale=self.simulation.estimate_scale((800, 800)))
            self.pygameWindow.simulate(self.simulation)

    
    def load(self) -> bool:
        # Make save folder
        saveFolder = os.path.join(self._directory, "saves")
        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)

        # Open file explorer
        file = filedialog.askopenfile(mode="r", defaultextension=".txt", initialdir=saveFolder, filetypes=(("Text file", "*.txt"), ))
        if file == None:
            return
        
        data = json.loads(file.read())

        # Remove all frames
        while len(self.frames) != 0:
            self.remove_frame_by_index(0)
        
        # Add correct number of frames, filling in details
        for i, frameData in enumerate(data):
            # Add frame
            self.add_frame()
            # Fill in data
            self.frames[i]["mass"][0].insert(0, frameData[0][0])
            self.frames[i]["mass"][1].set(frameData[0][1])
            # pos x
            self.frames[i]["pos"][0].insert(0, frameData[1][0])
            self.frames[i]["pos"][2].set(frameData[1][1])
            # pos y
            self.frames[i]["pos"][1].insert(0, frameData[2][0])
            self.frames[i]["pos"][3].set(frameData[2][1])
            # vel x
            self.frames[i]["vel"][0].insert(0, frameData[3][0])
            self.frames[i]["vel"][2].set(frameData[3][1])
            # vel y
            self.frames[i]["vel"][1].insert(0, frameData[4][0])
            self.frames[i]["vel"][3].set(frameData[4][1])
            # Colours
            self.frames[i]["col"][0].insert(0, frameData[5])
            self.frames[i]["col"][1].insert(0, frameData[6])
            self.frames[i]["col"][2].insert(0, frameData[7])
            # Name
            self.frames[i]["name"].delete(0, "end")
            self.frames[i]["name"].insert(0, frameData[8])
        
        return True
        
    
    def save(self):
        """Saves the values stored in input boxes to a file"""
        output = []
        if len(self.frames) == 0:
            # Throw error
            messagebox.showerror("Save cannot be empty", "Save Error\nA save cannot be empty!")
            return

        for frame in self.frames:
            output.append(self.getInputFromBoxes(frame))

        # Make save folder
        saveFolder = os.path.join(self._directory, "saves")
        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)

        # Open file explorer
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt", initialdir=saveFolder, filetypes=(("Text file", "*.txt"), ))
        if file == None:
            return
        file.write(json.dumps(output, indent=4))

    
    def getInputFromBoxes(self, frame):
        """Given a frame from ObjectFrame, gets the inputs out of the Entry boxes"""
        data = [
            [frame["mass"][0].get(), frame["mass"][1].get()],
            [frame["pos"][0].get(), frame["pos"][2].get()],
            [frame["pos"][1].get(), frame["pos"][3].get()],
            [frame["vel"][0].get(), frame["vel"][2].get()],
            [frame["vel"][1].get(), frame["vel"][3].get()],
            frame["col"][0].get(),
            frame["col"][1].get(),
            frame["col"][2].get(),
            frame["name"].get()
        ]

        # Remove leading and trailing spaces
        for i in range(len(data)):
            if isinstance(data[i], list):
                for j in range(len(data[i])):
                    data[i][j] = data[i][j].strip()
            else:
                data[i] = data[i].strip()


        return data


