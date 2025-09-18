import pygame
from gravity_sim.vector import Vector
from gravity_sim.simulation import Simulation


class Window:
    """Pygame window to display simulation."""
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.screen_size = Vector(600, 600)
        self.scale = self.estimate_scale()

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

    def scale_point(self, point: Vector, refPoint: Vector, scale: float) -> Vector:
        """Scale a point to render to the screen.

        Also flips the y position to render to the screen.

        Args:
            point (Vector): The point to scale.
            refPoint (Vector): The position of the "camera".
            scale (float): The scale or "zoom" to apply to the point.

        Returns:
            Vector: The scaled point.
        """
        point -= refPoint
        point *= scale
        point[0] = point[0] * -1

        return point

    def zoomIn(self):
        """Increase the scale of the simulation."""
        self._scale *= 1.2

    def zoomOut(self):
        """Decrease the scale of the simulation."""
        self._scale *= 0.8

    def estimate_scale(self) -> float:
        """Estimate an initial scale for the simulation based on the objects furthest apart.

        Returns:
            float: The estimated scale value.
        """
        if len(self.simulation.objects) < 2:
            return 1

        x_values = [obj.position[0] for obj in self.simulation.objects]
        y_values = [obj.position[1] for obj in self.simulation.objects]

        x_range = max(x_values) - min(x_values)
        y_range = max(y_values) - min(y_values)

        return max(self.screen_size[0], self.screen_size[1]) / max(x_range, y_range)
