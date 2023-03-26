import turtle, math

window = turtle.Screen()
window.title("A simulation of the movement of plantery bodies - Samuel Hartley")


# Constants
G = 6.67428e-11
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 200 / AU            # 200 px = 1 AU. 1 AU = dist from Earth to Sun
TIMESTEP = 24 * 3600          # 24 Hours

bodies = []

class object:
    def __init__(self, name, ID, mass, velocity, position, colour, sun=False):
        self.name = name
        self.ID = ID
        self.sun = sun
        self.mass = mass
        self.velocity = velocity
        self.position = position
        self.resultantforce = [0, 0]
        self.turtle = turtle.Turtle()
        self.colour = colour
        self.setupturtle()

    # Initialise turtle to represent position
    def setupturtle(self):
        self.turtle.penup()
        self.turtle.pencolor(self.colour)
        self.turtle.shape("circle")
        self.turtle.color(self.colour)
        self.turtle.speed(10)
        self.turtle.goto(self.position[0]*SCALE, self.position[1]*SCALE)
        # Only planets can have trails
        if self.sun == False:
            self.turtle.turtlesize(0.5)
            self.turtle.pendown()

    # Calculate forces that a body experinces
    def force(self, body):
        # Calculate the resultant force on yourself
        distance = [body.position[0] - self.position[0], body.position[1] - self.position[1]]

        # Find direct distance using pythag theorum
        directDistance = math.sqrt(distance[0]**2 + distance[1]**2)

        if directDistance == 0:
            raise ZeroDivisionError("Collision between two objects")


        # Calc direct force
        force = G * self.mass * body.mass / ((directDistance)**2)
        # Calc angle the force acts at
        theta = math.degrees(math.atan2(distance[1], distance[0]))

        # Resolve the force into x and y
        forceX = round(math.cos(math.radians(theta)) * force, 12)
        forceY = round(math.sin(math.radians(theta)) * force, 12)

        self.resultantforce[0] += forceX
        self.resultantforce[1] += forceY

    # Calculate diplacement using resultant force and update turtle
    def move(self):
        # Use resultant forces to move to a new place
        self.velocity[0] += self.resultantforce[0]/self.mass * TIMESTEP
        self.velocity[1] += self.resultantforce[1]/self.mass * TIMESTEP

        self.position[0] += self.velocity[0] * TIMESTEP
        self.position[1] += self.velocity[1] * TIMESTEP
 
        self.turtle.goto(self.position[0]*SCALE, self.position[1]*SCALE)

        self.resultantforce[0] = self.resultantforce[1] = 0


# Earth
bodies.append(object(
            name = "Earth",
            ID = len(bodies),
            mass = 5.9724e24,       # Mass in kg
            velocity = [0, 29780],  # Start velocity in m/s
            position = [AU, 0],     # Starting position in m
            colour = "blue"         # Turtle colour

))
# Mercury
bodies.append(object(
            name = "Mercury",
            ID = len(bodies),
            mass = 3.285e23,
            velocity = [0, 47000],
            position = [70000000 * 1000, 0],
            colour = "grey"

))
# Venus
bodies.append(object(
            name = "Venus",
            ID = len(bodies),
            mass = 4.867e24,
            velocity = [0, 35020],
            position = [108939000 * 1000, 0],
            colour = "brown"

))
# Mars
bodies.append(object(
            name = "Mars",
            ID = len(bodies),
            mass = 6.39e23,
            velocity = [0, 24007],
            position = [249200000 * 1000, 0],
            colour = "red"

))
# The Sun
bodies.append(object(
            name = "Sun",
            ID = len(bodies),
            mass = 1.98847e30,
            velocity = [0, 0],
            position = [0, 0],
            sun = True,
            colour = "yellow"

))

days = 0
years = 0

while True:
    days += 1
    if days > 365:
        days = 0
        years += 1
    # For each body
    for index in range(len(bodies)):
        # If you are not the sun
        if bodies[index].sun is not True:
            # Looop through all other bodies
            for externalObject in bodies:
                # Make sure this body is not yourself,  and only calculate forces from the sun 
                if externalObject.ID != bodies[index].ID and externalObject.sun == True:
                    bodies[index].force(externalObject)


        # After calulating resultant forces and storing them, move
        bodies[index].move()


    # Keeps track of time passed
    print("Days: %s     Years: %s" % (days, years))