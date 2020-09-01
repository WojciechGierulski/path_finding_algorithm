import pygame
import math
from params import Colors


class Spot:
    def __init__(self, row, col, width, total_rows, color=Colors.WHITE):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = color
        self.width = width
        self.neighbours = []
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == Colors.RED

    def is_wall(self):
        return self.color == Colors.BLACK

    def is_start(self):
        return self.color == Colors.ORANGE

    def is_end(self):
        return self.color == Colors.PURPLE

    def is_open(self):
        return self.color == Colors.GREEN

    def reset(self):
        self.color = Colors.WHITE

    def make_closed(self):
        self.color = Colors.RED

    def make_wall(self):
        self.color = Colors.BLACK

    def make_end(self):
        self.color = Colors.PURPLE

    def make_start(self):
        self.color = Colors.ORANGE

    def make_open(self):
        self.color = Colors.GREEN

    def make_white(self):
        self.color = Colors.WHITE

    def is_white(self):
        return self.color == Colors.WHITE

    def make_path(self):
        self.color = Colors.BLUE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False