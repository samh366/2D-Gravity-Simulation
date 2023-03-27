# Creates the pygame window to draw the simulation
import pygame

class Window():
    def __init__(self, screenSize, scale, fps=60):
        pygame.display.set_caption("Gravity Simulation  - All pairs algorithm")
        self.screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()

        self._fps = fps
        self._running = True
        self._scale = scale
        self._width = screenSize[0]
        self._height = screenSize[1]
        self._paused = False

    def _loop(self):
        """Loop to display the window"""
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        showLines = not showLines
                    
                    if event.key == pygame.K_SPACE:
                        self._paused = not self._paused

            self.screen.fill((0, 0, 0))
            # Draw objects
            self._drawObjects((0, 0))

            if not self._paused:
                self.__simulation.iterate()

            pygame.display.update()
            self.clock.tick(self._fps)

    def end(self):
        pygame.quit()
        quit()

    
    def simulate(self, simulation):
        """Takes in a simulation, and begins iterating through it."""
        self.__simulation = simulation
        self._loop()


    
    def _drawObjects(self, referencePoint):
        for coordinate, color in self.__simulation.objects(referencePoint, self._scale):
            # Draw object
            circle = (self._width//2 + coordinate[0], self._height//2 + coordinate[1])
            pygame.draw.circle(self.screen, color, circle, 8)
