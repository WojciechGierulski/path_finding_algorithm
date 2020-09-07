from queue import PriorityQueue
import time

timeout = 0.0001 # the smaller the timeout the faster the animation


class Algo:
    run = True

    @staticmethod
    def start(board, start_spot, end_spot, total_rows):
        Algo.run = True
        Algo.update_neighbours(board, total_rows)
        counter = 0
        open_set = PriorityQueue()
        open_set_hash = set()
        H_scores = {spot: float("inf") for row in board for spot in row}
        G_scores = {spot: float("inf") for row in board for spot in row}
        F_scores = {spot: float("inf") for row in board for spot in row}
        came_from = {spot: None for row in board for spot in row}
        H_scores[start_spot] = Algo.calculate_H_score(start_spot, end_spot)
        G_scores[start_spot] = 0
        F_scores[start_spot] = Algo.calculate_F_score(start_spot, G_scores, H_scores)
        open_set_hash.add(start_spot)
        open_set.put((0, counter, start_spot))
        counter += 1

        while not open_set.empty() and Algo.run:
            spot = open_set.get()[2]
            open_set_hash.remove(spot)

            if spot == end_spot:
                Algo.reconstruct_path(start_spot, end_spot, came_from)
                return True

            for neighbour in spot.neighbours:
                temp_g_score = G_scores[spot] + 1
                if temp_g_score < G_scores[neighbour]:
                    H_scores[neighbour] = Algo.calculate_H_score(neighbour, end_spot)
                    G_scores[neighbour] = temp_g_score
                    F_scores[neighbour] = Algo.calculate_F_score(neighbour, G_scores, H_scores)
                    came_from[neighbour] = spot
                    if neighbour not in open_set_hash:
                        counter += 1
                        open_set_hash.add(neighbour)
                        neighbour.make_open()
                        time.sleep(timeout)
                        open_set.put((F_scores[neighbour], counter, neighbour))

            if spot != start_spot:
                spot.make_closed()
                time.sleep(timeout)

        return False

    @staticmethod
    def update_neighbours(board, total_rows):
        for x in range(total_rows):
            for y in range(total_rows):

                if y - 1 >= 0:  # UP
                    if not board[x][y - 1].is_wall():
                        board[x][y].neighbours.append(board[x][y - 1])

                if y + 1 <= total_rows - 1:  # DOWN
                    if not board[x][y + 1].is_wall():
                        board[x][y].neighbours.append(board[x][y + 1])

                if x + 1 <= total_rows - 1:  # RIGHT
                    if not board[x + 1][y].is_wall():
                        board[x][y].neighbours.append(board[x + 1][y])

                if x - 1 >= 0:  # LEFT
                    if not board[x - 1][y].is_wall():
                        board[x][y].neighbours.append(board[x - 1][y])

    @staticmethod
    def calculate_H_score(spot1, end_spot):
        return abs(end_spot.row - spot1.row) + abs(end_spot.col - spot1.col)

    @staticmethod
    def calculate_G_score(previous_spot, g_scores):
        return 1 + g_scores[previous_spot]

    @staticmethod
    def calculate_F_score(spot, g_scores, h_scores):
        return g_scores[spot] + h_scores[spot]

    @staticmethod
    def reconstruct_path(start, end, came_from):
        spot = end
        while spot != start:
            spot.make_path()
            spot = came_from[spot]
