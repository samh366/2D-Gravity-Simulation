import math

G = 6.67428e-11 # Gravitational constant

# Simulates the movement of objects
class Simulation:
    def __init__(self, objects, timestep=24*3600, iterations=8):
        self._timestep = timestep
        self._timePassed = 0
        self._objects = list(objects)
        self._iterations = iterations

    def set_timestep(self, timestep):
        if timestep > 0:
            self._timestep = timestep

    def calc_force(self, object1, object2):
        """
        Calculates the force object2 exertes on object1.
        Then adds this force to the object's total force for this simulation frame.

        Args:
            object1: An instance of Object
            object2: An instance of Object, exertes force on object1
        """

        # object2[0] returns the x coordinate of object2
        distance = [object2[0] - object1[0], object2[1] - object1[1]]
        directDistance = math.sqrt(distance[0]**2 + distance[1]**2)

        if directDistance == 0:
            return

        # Calculate the force between the objects
        force = G * object1.mass * object2.mass / ((directDistance)**2)
        # Calculate angle the force acts at
        theta = math.degrees(math.atan2(distance[1], distance[0]))

        # Calculate the x and y components of each force
        forceX = round(math.cos(math.radians(theta)) * force, 12)
        forceY = round(math.sin(math.radians(theta)) * force, 12)

        object1.add_force(forceX, forceY)

    
    def move_objects(self, timestep):
        """Moves the objects in the simulation based on the forces acting on them."""

        for obj in self._objects:
            # Use resultant force to move the object to a new place
            obj.velocity[0] += obj.force[0]/obj.mass * timestep
            obj.velocity[1] += obj.force[1]/obj.mass * timestep

            obj.pos[0] += obj.velocity[0] * timestep
            obj.pos[1] += obj.velocity[1] * timestep

            obj.reset_force()


    def scaled_objects(self, refPoint, scale):
        """
        A generator to adjust each objects coordinates to a reference point and to scale,
        returning this value and the color of the object.
        Also returns an index
        """
        for index, obj in enumerate(self._objects):
            yield index, (
                    obj.adjust_and_scale(refPoint, scale),
                    obj.color)
            
    
    def object_data(self):
        """Just returns the raw object data"""
        for obj in self._objects:
            yield obj

    
    def get_object(self, index):
        """Return data about a specific object"""
        if index < 0 or index >= len(self._objects):
            return None
        return self._objects[index]
            
    
    def estimate_scale(self, screenSize):
        """Estimates the most appropriate scale for the simulation"""
        if len(self._objects) == 1:
            return screenSize[0]
        # Add a bit of padding
        screenSize = [round(screenSize[0]*0.9), round(screenSize[1]*0.9)]

        # Find highest and lowest x and y values
        range = 0
        x = [self._objects[0][0], self._objects[0][0]]
        y = [self._objects[0][1], self._objects[0][1]]

        for obj in self._objects:
            if obj[0] < x[0]:   # Smaller x
                x[0] = obj[0]
            if obj[0] > x[1]:   # Greater x
                x[1] = obj[0]
            if obj[1] < y[0]:   # Smaller y
                y[0] = obj[1]
            if obj[1] > y[1]:   # Greater y
                x[0] = obj[1]
        
        xRange = x[1]-x[0]
        yRange = y[1]-y[0]

        if xRange > yRange:
            range = xRange
        else:
            range = yRange
        

        return (screenSize[0]//2)/range
    
    def num_objects(self) -> int:
        """Returns the number of objects being simulated"""
        return len(self._objects)
    

    def iterate(self):
        """Advances the simulation by a set time frame"""
        # Iterate x number of times for greater accuracy
        timestep = self._timestep // self._iterations
        for i in range(self._iterations):
            # n^2 efficiency, can be improved using Barnes Hut Algorithm
            for obj1 in self._objects:
                for obj2 in self._objects:
                    # If not overlapping, also catches same objects
                    if obj1.pos != obj2.pos:
                        # Calc force obj2 exertes on obj1
                        self.calc_force(obj1, obj2)

            self.move_objects(timestep)
            self._timePassed += timestep



