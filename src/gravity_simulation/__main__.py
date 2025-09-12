from gravity_simulation.cli import handle_cli
from gravity_simulation.simulation import Simulation

def main():
    args = handle_cli()
    Simulation()
    print(args)