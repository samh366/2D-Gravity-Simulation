# The class for an object in the simulation
import random
class Object:
    def __init__(
            self,
            mass: float,
            pos: tuple[float, float],
            velocity: tuple[float, float],
            color: tuple[int, int, int]):

        self.mass = mass
        self.pos = pos
        self.velocity = velocity
        # Assign random color
        if color == (-1, -1, -1):
            self.color = (random.randint(0, 255) for i in range(3))
        else:
            self.color = color

        # The force the object experiences from other objects
        self.force = [0, 0]

    
    def add_force(self, x, y):
        self._force = [self._force[0]+x, self._force[1]+y]

    def reset_force(self):
        self._force = [0, 0]

    def adjust_and_scale(self, refPoint, scale):
        """Adjusts an object's coordinates to a reference point and scales them"""
        x = self.pos[0] - refPoint[0]
        y = self.pos[1] - refPoint[1]

        return (x*scale, y*scale)
    
    # Access position of the object by indexing
    def __getitem__(self, key):
        return self._pos[key]

    def __setitem__(self, key, value):
        if key > -3 and key < 2:
            self._pos[key] = float(value)
        else:
            raise IndexError("Cannot asign position in more than 2 dimensions")