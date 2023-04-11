# The class for an object in the simulation
import random
class Object:
    def __init__(
            self,
            mass: float,
            pos: tuple[float, float],
            velocity: tuple[float, float],
            color: tuple[int, int, int],
            name = ""):

        self.mass = mass
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.name = name
        # Assign random color
        if color == (-1, -1, -1):
            self.color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
        else:
            self.color = color

        # The force the object experiences from other objects
        self.force = [0, 0]

    
    def add_force(self, x, y):
        self.force = [self.force[0]+x, self.force[1]+y]

    def reset_force(self):
        self.force = [0, 0]
    
    def hasName(self):
        return self.name != ""

    def adjust_and_scale(self, refPoint, scale):
        """Adjusts an object's coordinates to a reference point and scales them"""
        x = self.pos[0] - refPoint[0]
        y = self.pos[1] - refPoint[1]

        # Due to pygame's coordinate system, flip y values
        return (x*scale, y*scale*-1)
    
    # Access position of the object by indexing
    def __getitem__(self, key):
        return self.pos[key]

    def __setitem__(self, key, value):
        if key > -3 and key < 2:
            self.pos[key] = float(value)
        else:
            raise IndexError("Cannot asign position in more than 2 dimensions")