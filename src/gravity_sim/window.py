import pygame
from gravity_sim.vector import Vector
from gravity_sim.simulation import Simulation
from gravity_sim.object import Color
from pygame.event import Event


class Window:
    """Pygame window to display simulation."""

    def __init__(self, simulation: Simulation):
        """Intialise a new Window to render a simulation.

        Args:
            simulation (Simulation): The simulation to start rendering.
        """
        self.simulation = simulation

        self._fps = 60
        self.screen_size = Vector(600, 600)
        self.camera_pos = Vector(0, 0)
        self.scale = self.estimate_scale()

        pygame.display.set_caption("Gravity Simulation")
        self.screen = pygame.display.set_mode(tuple(self.screen_size), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.paused = False
        self.focused_object = None
        self.zoom_factor = 1.2

    def run(self):
        """Start the window to render the simulation."""
        while 1:
            result = self.update()
            if not result:
                break
        pygame.quit()

    def update(self) -> bool:
        """Update loop for window and simulation logic.

        Returns:
            bool: True if the simulation should continue, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                self.handle_event(event)

        self.screen.fill((0, 0, 0))
        self.move_camera()
        self.update_simulation()
        self.focus_camera()
        self.render_simulation()

        pygame.display.update()
        self.clock.tick(self._fps)

        return True

    def update_simulation(self):
        """Update the simulation to the next state."""
        if not self.paused:
            self.simulation.step()

    def handle_event(self, event: Event) -> None:
        """Update the simulation's status based on pygame event.

        Args:
            event (Event): A pygame event.
        """
        match event.type:
            case pygame.MOUSEWHEEL:
                self.handle_zoom(event.y)
                return
            case pygame.KEYDOWN:
                self.handle_key_down(event.key)
                return

    def handle_key_down(self, key: int) -> None:
        """Update the status of the simulation based on a key down press.

        Args:
            key (int): The key pressed.
        """
        if key == pygame.K_SPACE:
            self.toggle_pause()
        if key == pygame.K_RIGHT:
            self.update_focused_object_index(1)
        if key == pygame.K_LEFT:
            self.update_focused_object_index(-1)

    def toggle_pause(self) -> None:
        """Toggle the simulation between paused and unpaused."""
        self.paused = not self.paused

    def move_camera(self):
        """If the left mouse button is held, moves the camera."""
        self.mouse_movement = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            self.focused_object = None
            self.camera_pos -= Vector(self.mouse_movement[0], self.mouse_movement[1]*-1)

    def update_focused_object_index(self, amount: int) -> None:
        """Change the index of the focused object by an amount.

        Args:
            amount (int): The amount to change the focused object by.
        """
        self.camera_pos = Vector(0, 0)
        if self.focused_object is None:
            self.focused_object = -1
        self.focused_object += amount

        if self.focused_object >= self.simulation.get_num_objects():
            self.focused_object = 0
        if self.focused_object < 0:
            self.focused_object = self.simulation.get_num_objects() - 1

    def focus_camera(self):
        """Set the cameras position to the location of the focused object."""
        if self.focused_object is not None:
            self.camera_pos = self.simulation.get_object(self.focused_object).position * self.scale

    def handle_zoom(self, y: int) -> None:
        """Zoom in or out based on the mouse wheel movement.

        Args:
            y (int): Y value of the mouse wheel event.
        """
        if y > 0:
            self.zoom_in()
        elif y < 0:
            self.zoom_out()

    def render_simulation(self):
        """Draw all the objects on the screen."""
        for obj in self.simulation.get_objects():
            pos = self.scale_point(obj.get_position(), self.camera_pos)
            self.draw_point(pos, obj.color)

    def draw_point(self, position: Vector, color: Color) -> None:
        """Draw a point on the screen at the given position, centering the point on the screen.

        Args:
            position (Vector): The position to draw the point.
            color (Color): Color of the point.
        """
        width, height = self.screen.get_size()
        position += Vector(width // 2, height // 2)
        pygame.draw.circle(surface=self.screen, color=tuple(color), center=tuple(position), radius=8)

    def scale_point(self, point: Vector, refPoint: Vector) -> Vector:
        """Scale a point to render to the screen.

        Also flips the y position to render to the screen.

        Args:
            point (Vector): The point to scale.
            refPoint (Vector): The position of the "camera".

        Returns:
            Vector: The scaled point.
        """
        point *= self.scale
        point -= refPoint
        return Vector(point[0], point[1] * -1)

    def zoom_in(self):
        """Increase the scale of the simulation."""
        self.scale *= self.zoom_factor
        self.camera_pos *= self.zoom_factor

    def zoom_out(self):
        """Decrease the scale of the simulation."""
        self.scale /= self.zoom_factor
        self.camera_pos /= self.zoom_factor

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
