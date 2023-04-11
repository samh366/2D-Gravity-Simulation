import os
import pygame

from classes.configMenu import ConfigMenu


def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    window = ConfigMenu(dir)
    window.open()
    pygame.quit()



if __name__ == "__main__":
    main()