# Creates the pygame window to draw the simulation
import pygame

class Window():
    def __init__(self, screenSize, scale):
        pygame.display.set_caption("Gravity Simulation  - All pairs algorithm")
        self.screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()

        self._running = True
        self._scale = scale
        self._width = screenSize[0]
        self._height = screenSize[1]

    def loop(self):
        """Loop to display the window"""
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        showLines = not showLines
                    
                    if event.key == pygame.K_SPACE:
                        pause = not pause

            self.screen.fill((0, 255, 0))
            pygame.display.update()
            self.clock.tick(60)

    def end(self):
        pygame.quit()
        quit()

    
    def drawObjects(self, simulation, referencePoint):
        for coordinate, color in simulation.objects(referencePoint, self._scale):
            # Draw object
            circle = (self._width//2 + coordinate[0], self._height//2 + coordinate[1])
            pygame.draw.circle(self.screen, color, circle, 8)


win = Window((800, 800))
win.loop()