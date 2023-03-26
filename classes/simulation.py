import math

G = 6.67428e-11
TIMESTEP = 24 * 3600          # 24 Hours

# Simulates the movement of objects
class Simulation:
    def __init__(self, *args):
        self._objects = [i for i in args]


    def calc_force(self, object1, object2):
        """
        Calculates the force object2 exertes on object1.
        Then adds this force to the object's total force for this simulation frame.

        Args:
            object1: An instance of Object
            object2: An instance of Object, exertes force on object1
        """

        # object2[0] returns the x coordinate of object2
        distance = [object2[0] - self[0], object2[1] - self[1]]
        directDistance = math.sqrt(distance[0]**2 + distance[1]**2)

        if directDistance == 0:
            raise ZeroDivisionError("Collision between two objects")

        # Calculate the force between the objects
        force = G * self._mass * object2.mass / ((directDistance)**2)
        # Calc angle the force acts at
        theta = math.degrees(math.atan2(distance[1], distance[0]))

        # Calculate the x and y components of each force
        forceX = round(math.cos(math.radians(theta)) * force, 12)
        forceY = round(math.sin(math.radians(theta)) * force, 12)

        object1.add_force(forceX, forceY)

    
    def move_objects(self):
        """Moves the objects in the simulation based on the forces acting on them."""

        for obj in self._objects:
            # Use resultant force to move the object to a new place
            obj.velocity[0] += obj.resultantforce[0]/obj.mass * TIMESTEP
            obj.velocity[1] += obj.resultantforce[1]/obj.mass * TIMESTEP

            obj.pos[0] += obj.velocity[0] * TIMESTEP
            obj.pos[1] += obj.velocity[1] * TIMESTEP

            obj.reset_force()

    # Use a generator to request object data in the simulation
    def objects(self, refPoint, scale):
        """
        A generator to adjust each objects coordinates to a reference point and to scale,
        returning this value and the color of the object
        """
        for obj in self._objects:
            yield (
                    obj.adjust_and_scale(refPoint, scale),
                    obj.color)
            
    
    def estimate_scale(self, screenSize):
        """Estimates the most appropriate scale for the simulation"""
        # Find highest and lowest x and y values
        range = 0
        x = [None, None]
        y = [None, None]

        for obj in self._objects:
            if obj[0] < x[0] or x[0] == None:
                x[0] = obj[0]
            if obj[0] > x[1] or x[1] == None:
                x[1] = obj[0]
            if obj[1] < y[0] or y[0] == None:
                y[0] = obj[1]
            if obj[1] > y[1] or y[1] == None:
                x[0] = obj[1]
        
        xRange = x[1]-x[0]
        yRange = y[1]-y[0]

        if xRange > yRange:
            range = xRange
        else:
            range = yRange
        

        return (screenSize//2)/yRange

