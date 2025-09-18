import pygame
from gravity_sim.simulation import Simulation


class Window:
    """Pygame window to display simulation."""
    def __init__(self, simulation: Simulation):
        self.simulation = simulation

        pygame.display.set_caption("Gravity Simulation")
        self.screen = pygame.display.set_mode(size=(600, 600))
        self.clock = pygame.time.Clock()


    def run(self):
        while 1:
            result = self.update()
            if not result:
                break
        pygame.quit()

    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.simulation.step()
        self.render_simulation()
        
        return True
    
    def render_simulation(self):
        pass