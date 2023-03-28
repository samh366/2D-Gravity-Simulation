import random, math

from classes.object import Object
from classes.pygameWindow import Window
from classes.simulation import Simulation

TIMESTEP = 24 * 3600 // 1.5
AU = (149.6e6 * 1000)
G = 6.67428e-11

# Temporary
objects = [
    # Sun
    Object(
            mass=1.98847e30,
            pos=(0, 0),
            velocity=(0, 0),
            color=(224, 214, 13)),

    # Earth
    Object(
        mass=5.9724e24,
        pos=(AU, 0),
        velocity=(0, 29780*0.5), # 29780
        color=(13, 125, 222))
]

def randNum():
    num = random.randint(-AU*10, AU*10)
    while (num < AU*0.8 and num > -AU*0.8):
        num = random.randint(-AU, AU)
    
    return num


for i in range(50):
    dist = random.randint(AU*0.2, AU*1.5)
    v = math.sqrt((G*1.98847e30)/dist)  # Calc orbital speed
    angle = random.randint(0, 360)    # Random angle
    # Translate pos
    Px = dist*math.cos(math.radians(angle))
    Py = dist*math.sin(math.radians(angle))
    # Translate V
    Vx = -math.sin(math.radians(angle))*v
    Vy = math.cos(math.radians(angle))*v

    objects.append(
        Object(
            mass=random.randint(1, 1000)*10e22,
            pos=[Px, Py, 0],
            velocity=[Vx, Vy, 0],
            color=(-1, -1, -1))
    )


def main():
    # Init planets
    sim = Simulation(objects, TIMESTEP)
    window = Window((800, 800), sim.estimate_scale((800, 800)), fps=60)
    window.simulate(sim)


if __name__ == "__main__":
    main()
# Call end