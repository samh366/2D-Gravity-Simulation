from gravity_sim.config_loader import ConfigLoader
from gravity_sim.simulation import Simulation
from gravity_sim.window import Window

class SimulationRunner:
    """Loads and starts simulations."""

    def run(self, config_file: str):
        """Load a simulation from the given config file and display it in a window.

        Args:
            config_file (str): The config file to load the simulation's starting state from.
        """
        sim = ConfigLoader.load_file(config_file)
        window = Window(sim)
        window.run()
