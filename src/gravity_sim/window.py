import pygame
from gravity_sim.vector import Vector
from gravity_sim.simulation import Simulation
from gravity_sim.object import Color


class Window:
    """Pygame window to display simulation."""

    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.width, self.height = self.screen_size
        self.scale = self.estimate_scale()

        self._fps = 60
        self.screen_size = Vector(600, 600)
        self.camera_pos = Vector(0, 0)

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

            if event.type == pygame.MOUSEWHEEL:
                self.handle_zoom(event.y)

        self.simulation.step()
        self.render_simulation()

        pygame.display.update()
        self.clock.tick(self._fps)

        return True

    def handle_zoom(self, y: int) -> None:
        """Zoom in or out based on the mouse wheel movement.

        Args:
            y (int): Y value of the mouse wheel event.
        """
        if y > 0:
            self.zoomIn()
        elif y < 0:
            self.zoomOut()

    def render_simulation(self):
        """Draw all the objects on the screen."""
        for object in self.simulation.objects:
            pos = self.scale_point(object.get_position(), self.camera_pos, self.scale)
            self.draw_point(pos, object.color)

    def draw_point(self, position: Vector, color: Color) -> None:
        """Draw a point on the screen at the given position, centering the point on the screen.

        Args:
            position (Vector): The position to draw the point.
            color (Color): Color of the point.
        """
        position += Vector(self.width // 2, self.height // 2)
        pygame.draw.circle(surface=self.screen, color=tuple(color), position=tuple(position), radius=8)

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
