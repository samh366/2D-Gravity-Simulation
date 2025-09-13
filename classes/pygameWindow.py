# Creates the pygame window to draw the simulation
import pygame


class Window:
    def __init__(self, screenSize, scale, fps=60):
        """A pygame window to display the simulation"""
        pygame.display.set_caption("Gravity Simulation  - All pairs algorithm")
        self.screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()

        self._fps = fps
        self._running = True
        self._scale = scale
        self._originalScale = scale
        self._width = screenSize[0]
        self._height = screenSize[1]
        self._paused = False
        self._focusObject = -1

        self._showNames = True

        # Overlay
        self.font = pygame.font.SysFont("Calibri", 20)
        self._help = self.font.render("H - Help", True, (255, 255, 255))
        text = (
            "F2 - Reset Zoom",
            "F3 - Hide/Show Names",
            "Left Arrow - Decrement focused object",
            "Right Arrow - Increment focused object",
            "F4 - Reset Focus",
            "space - Pause/Unpause",
        )
        self._overlay = pygame.Surface(screenSize, pygame.SRCALPHA, 32).convert_alpha()
        self._showOverlay = False
        # Overlay to blit names to
        self._nameOverlay = pygame.Surface(screenSize, pygame.SRCALPHA, 32).convert_alpha()

        for i, txt in enumerate(text):
            self._overlay.blit(self.font.render(txt, True, (255, 255, 255)), (5, 5 + (i * 20)))

    def overlay(self):
        self._showOverlay = not self._showOverlay

    def names(self):
        self._showNames = not self._showNames

    def resetScale(self):
        self._scale = self._originalScale

    def _loop(self):
        """Loop to display the window"""
        keyBindings = {
            pygame.K_SPACE: self.pause,
            pygame.K_h: self.overlay,
            pygame.K_F2: self.resetScale,
            pygame.K_F3: self.names,
            pygame.K_LEFT: self.decrementFocus,
            pygame.K_RIGHT: self.incrementFocus,
            pygame.K_F4: self.resetFocus,
        }

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    self.end()
                    return

                # Check pressed keys
                if event.type == pygame.KEYDOWN:
                    for key in keyBindings.keys():
                        if event.key == key:
                            keyBindings[key]()

                # Zoom in and out
                if event.type == pygame.MOUSEWHEEL:
                    # Scroll up
                    if event.y > 0:
                        self.zoomIn()
                    # Scroll down
                    elif event.y < 0:
                        self.zoomOut()

            self.screen.fill((0, 0, 0))
            # Draw objects, finding the refernce point to draw from
            if self._focusObject == -1:
                self._drawObjects((0, 0))
            else:
                self._drawObjects(self.__simulation.get_object(self._focusObject).pos)

            # Object names
            if self._showNames == True:
                self.screen.blit(self._nameOverlay, (0, 0))

            # Overlay
            if self._showOverlay == True:
                self.blitOverlay()
            else:
                self.blitHelp()

            # Show focused object
            if self._focusObject == -1:
                text = self.font.render("Focused Object: None", True, (255, 255, 255))
            else:
                text = self.font.render(
                    "Focused Object: " + self.__simulation.get_object(self._focusObject).name, True, (255, 255, 255)
                )

            self.screen.blit(text, (5, self._height - 30))

            if not self._paused:
                self.__simulation.iterate()

            pygame.display.update()
            self.clock.tick(self._fps)

    def end(self):
        pygame.quit()

    def simulate(self, simulation):
        """Takes in a simulation, and begins iterating through it."""
        self.__simulation = simulation
        self._renderNames()
        self._loop()

    def zoomIn(self):
        self._scale = self._scale * 1.2

    def zoomOut(self):
        self._scale = self._scale * 0.8

    def blitHelp(self):
        self.screen.blit(self._help, (5, self._height - 60))

    def blitOverlay(self):
        self.screen.blit(self._overlay, (0, 0))

    def incrementFocus(self):
        self._focusObject += 1
        if self._focusObject >= self.__simulation.num_objects():
            self._focusObject = -1

    def decrementFocus(self):
        self._focusObject -= 1
        if self._focusObject < -1:
            self._focusObject = self.__simulation.num_objects() - 1

    def resetFocus(self):
        self._focusObject = -1

    def pause(self):
        self._paused = not self._paused

    def _drawObjects(self, referencePoint):
        """Draw the simulation objects and their names to the screen"""
        self._nameOverlay.fill(pygame.Color(0, 0, 0, 0))
        for index, (coordinate, color) in self.__simulation.scaled_objects(referencePoint, self._scale):
            # Draw object
            circle = (self._width // 2 + coordinate[0], self._height // 2 + coordinate[1])
            pygame.draw.circle(self.screen, color, circle, 8)
            # Draw name
            if self._showNames == True:
                self._nameOverlay.blit(
                    self._names[index], (circle[0] - self._names[index].get_width() // 2, circle[1] - 35)
                )

    def _renderNames(self):
        """Pre render object names"""
        self._names = []
        for object in self.__simulation.object_data():
            self._names.append(self.font.render(object.name, True, object.color))
