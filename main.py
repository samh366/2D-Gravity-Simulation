from classes.pygameWindow import Window
from classes.object import Object
from classes.simulation import Simulation

TIMESTEP = 24 * 3600 // 2
AU = (149.6e6 * 1000)

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
        velocity=(0, 29780),
        color=(13, 125, 222))
]

def main():
    # Init planets
    sim = Simulation(objects, TIMESTEP)
    window = Window((800, 800), sim.estimate_scale((800, 800)), fps=60)
    window.simulate(sim)


if __name__ == "__main__":
    main()
# Call end