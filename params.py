import pygame
pygame.init()

class Params:
    WIDTH = 660
    ROWS = 55
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finder")
    spot_width = 12


class Colors:
    ORANGE = (255,165,0)
    SHADOW = (192, 192, 192)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 128)
    RED = (200, 0, 0)
    PURPLE = (177, 156, 217)