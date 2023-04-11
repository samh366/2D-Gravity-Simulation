# 2D-Gravity-Simulation
 A simple, customisable simulation of 2D gravity.
 Visualised using Pygame and configured using a Tkinter window.
 Includes the ability to save and load simulation configurations.
 Uses the all-pairs algorithm, every object is compared to every other object.
 This could be improved using the Barnest Hut algorithm, which I may implement in the future.
 
 Given an array of gravitational objects treated as point masses, the simulation best estimates how these objects will interact with each other.
 Using the mass and positions of several points, the forces between them can be calculated and thus their resultant acceleration.
 
 + Includes saving and loading
 + Customisable simulation starting points
 + Refocus which object is being viewed in the simulation
 + View object names during the simulation
 + Infinitely adjust the scale by scrolling up or down
 
 Big thanks to mp035 on Github for his scrollable frame widget in Tkinter.
 This code can be found in the scrollableFrame.py file contained in the classes folder.
