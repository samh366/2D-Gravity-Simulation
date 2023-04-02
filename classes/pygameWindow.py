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
        self._originalScale = scale
        self._width = screenSize[0]
        self._height = screenSize[1]
        self._paused = False

        # Overlay
        font = pygame.font.SysFont("Calibri", 20)
        self._help = font.render("H - Help", True, (255, 255, 255))
        text = (
            "F2 - Reset Zoom",
            "F3 - Big Test",
            "F3 - Big Test",
            "F3 - Big Test",
            "F3 - Big Test",
            "F3 - Big Test"
        )
        self._overlay = pygame.Surface(screenSize, pygame.SRCALPHA, 32).convert_alpha()
        self._showOverlay = False

        for i, txt in enumerate(text):
            self._overlay.blit(font.render(txt, True, (255, 255, 255)), (5, 5+(i*20)))

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

                    if event.key == pygame.K_h:
                        self._showOverlay = not self._showOverlay

                    if event.key == pygame.K_F2:
                        self._scale = self._originalScale

                if event.type == pygame.MOUSEWHEEL:
                    # Scroll up
                    if event.y > 0:
                        self.zoomIn()
                    elif event.y < 0:
                        self.zoomOut()



            self.screen.fill((0, 0, 0))
            # Draw objects
            self._drawObjects((0, 0))

            # Overlay
            if self._showOverlay == True:
                self.blitOverlay()
            else:
                self.blitHelp()

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


    def zoomIn(self):
        self._scale = self._scale * 1.2
    
    def zoomOut(self):
        self._scale = self._scale * 0.8

    def blitHelp(self):
        self.screen.blit(self._help, (5, self._height-30))

    def blitOverlay(self):
        self.screen.blit(self._overlay, (0, 0))


    
    def _drawObjects(self, referencePoint):
        for coordinate, color in self.__simulation.objects(referencePoint, self._scale):
            # Draw object
            circle = (self._width//2 + coordinate[0], self._height//2 + coordinate[1])
            pygame.draw.circle(self.screen, color, circle, 8)
