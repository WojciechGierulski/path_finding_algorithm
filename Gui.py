import pygame
from spot import Spot
from params import Params, Colors
import threading
from algorithm import Algo
import sys


class Draw:
    @staticmethod
    def create_board(rows):
        board = []
        for x in range(rows):
            board.append([])
            for y in range(rows):
                board[x].append(Spot(y, x, Params.spot_width, Params.ROWS))
        return board

    @staticmethod
    def draw_grid(screen, spot_width, total_rows, screen_width):
        for i in range(total_rows):
            pygame.draw.line(screen, Colors.SHADOW, (i * spot_width, 0), (i * spot_width, screen_width), 1)
            pygame.draw.line(screen, Colors.SHADOW, (0, i * spot_width), (screen_width, i * spot_width), 1)

    @staticmethod
    def draw_spots(board, screen):
        for x in board:
            for spot in x:
                spot.draw(screen)


class GUI:
    def __init__(self):
        self.start = None
        self.end = None
        self.run = False
        self.solving = False

    def get_spot_on_mouse(self, position, spot_width, board, screen_width):
        xm, ym = position
        if xm >= 0 and xm <= screen_width and ym >= 0 and ym <= screen_width:
            x = xm // spot_width
            y = ym // spot_width
            return board[x][y]
        else:
            return None

    def check_click(self, position, board):
        spot = self.get_spot_on_mouse(position, Params.spot_width, board, Params.WIDTH)
        if spot and not self.solving:
            if self.start is None:
                spot.make_start()
                self.start = spot
            elif self.end is None and spot != self.start:
                spot.make_end()
                self.end = spot
            elif spot.is_wall():
                spot.make_white()

    def wall_making(self, position, board, mouse_button_hold):
        spot = self.get_spot_on_mouse(position, Params.spot_width, board, Params.WIDTH)
        if spot and not self.solving and mouse_button_hold:
            if not spot.is_end() and not spot.is_start():
                clearing = pygame.key.get_pressed()[pygame.K_c]
                if not spot.is_wall() and not clearing:
                    spot.make_wall()
                elif spot.is_wall() and clearing:
                    spot.make_white()

    def mainloop(self):
        self.run = True
        mouse_button_hold = False
        thread = None
        board = Draw.create_board(Params.ROWS)
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    Algo.run = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.solving:
                    self.check_click(pygame.mouse.get_pos(), board)
                    mouse_button_hold = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_button_hold = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.solving:
                        self.solving = True
                        thread = threading.Thread(target=Algo.start,
                                                args=(board, self.start, self.end, Params.ROWS))
                        thread.start()
                    elif event.key == pygame.K_r:
                        # RESTART
                        thread = None
                        self.start = None
                        self.end = None
                        self.solving = False
                        board = Draw.create_board(Params.ROWS)
                if self.end and self.start:
                    self.wall_making(pygame.mouse.get_pos(), board, mouse_button_hold)
            Draw.draw_spots(board, Params.screen)
            Draw.draw_grid(Params.screen, Params.spot_width, Params.ROWS, Params.WIDTH)
            pygame.display.update()
