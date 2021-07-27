import pygame as pg
import board

grey = (50, 50, 50)
dark_grey = (20, 20, 20)
green = (50, 150, 50)
red = (150, 50, 50)
bright_red = (200, 100, 100)


class Renderer:

    def __init__(self, board_size_x: int, board_size_y: int, snake_size):
        self.board_size_x = board_size_x
        self.board_size_y = board_size_y
        self.snake_size = snake_size
        if not pg.init():
            exit(1)
        self.dis = pg.display.set_mode((board_size_x * (snake_size + 1) + 1, board_size_y * (snake_size + 1) + 1))
        self.dis.fill(grey)
        for i in range(board_size_x + 1):
            pg.draw.line(self.dis, dark_grey, (i * (snake_size + 1), 0),
                         (i * (snake_size + 1), board_size_y * (snake_size + 1) + 1))

        for i in range(board_size_y + 1):
            pg.draw.line(self.dis, dark_grey, (0, i * (snake_size + 1)),
                         (board_size_x * (snake_size + 1) + 1, i * (snake_size + 1)))
        pg.display.update()
        pg.display.set_caption("Snake")

    def render_scene(self, board_instance: board, route: list[(int, int)]):
        self.dis.fill(grey)
        for i in range(self.board_size_x + 1):
            pg.draw.line(self.dis, dark_grey, (i * (self.snake_size + 1), 0),
                         (i * (self.snake_size + 1), self.board_size_y * (self.snake_size + 1) + 1))

        for i in range(self.board_size_y + 1):
            pg.draw.line(self.dis, dark_grey, (0, i * (self.snake_size + 1)),
                         (self.board_size_x * (self.snake_size + 1) + 1, i * (self.snake_size + 1)))

        self.draw_head(board_instance)
        self.draw_tail(board_instance)
        self.draw_snake(board_instance)
        self.draw_planned(route)
        for x in range(len(board_instance.board)):
            for y in range(len(board_instance.board[x])):
                """if board_instance.board[x][y] == board.CellType.SNAKE:
                    pg.draw.rect(self.dis, green,
                                 [x * (self.snake_size + 1),
                                  y * (self.snake_size + 1),
                                  self.snake_size+2,
                                  self.snake_size+2])"""
                if board_instance.board[x][y] == board.CellType.APPLE:
                    pg.draw.circle(self.dis, red,
                                   [x * (self.snake_size + 1) + 1 + self.snake_size / 2,
                                    y * (self.snake_size + 1) + 1 + self.snake_size / 2],
                                   self.snake_size / 2)

    def draw_head(self, board_instance: board):
        pg.draw.circle(self.dis, green,
                       [board_instance.snake[0][0] * (self.snake_size + 1) + 1 + self.snake_size / 2,
                        board_instance.snake[0][1] * (self.snake_size + 1) + 1 + self.snake_size / 2],
                       self.snake_size / 3)
        if len(board_instance.snake) > 1:
            # right predecessor
            if board_instance.snake[0][0] - board_instance.snake[1][0] == -1 or \
                    board_instance.snake[0][0] - board_instance.snake[1][0] == len(board_instance.board) - 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[0][0] * (self.snake_size + 1) + self.snake_size / 2 + 1,
                              board_instance.snake[0][1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              self.snake_size / 2 + 1,
                              (self.snake_size / 3) * 2])
            elif board_instance.snake[0][0] - board_instance.snake[1][0] == 1 or \
                    board_instance.snake[0][0] - board_instance.snake[1][0] == -len(board_instance.board) + 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[0][0] * (self.snake_size + 1),
                              board_instance.snake[0][1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              self.snake_size / 2 + 1,
                              (self.snake_size / 3) * 2])
            elif board_instance.snake[0][1] - board_instance.snake[1][1] == 1 or \
                    board_instance.snake[0][1] - board_instance.snake[1][1] == -len(board_instance.board[0]) + 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[0][0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              board_instance.snake[0][1] * (self.snake_size + 1),
                              (self.snake_size / 3) * 2,
                              self.snake_size / 2 + 1])
            elif board_instance.snake[0][1] - board_instance.snake[1][1] == -1 or \
                    board_instance.snake[0][1] - board_instance.snake[1][1] == len(board_instance.board[0]) - 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[0][0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              board_instance.snake[0][1] * (self.snake_size + 1) + self.snake_size / 2 + 1,
                              (self.snake_size / 3) * 2,
                              self.snake_size / 2 + 1])

    def draw_tail(self, board_instance: board):
        if len(board_instance.snake) > 1:
            tail_idx = len(board_instance.snake) - 1
            pg.draw.circle(self.dis, green,
                           [board_instance.snake[tail_idx][0] * (self.snake_size + 1) + 1 + self.snake_size / 2,
                            board_instance.snake[tail_idx][1] * (self.snake_size + 1) + 1 + self.snake_size / 2],
                           self.snake_size / 3)

            # right predecessor
            if board_instance.snake[tail_idx][0] - board_instance.snake[tail_idx - 1][0] == -1 or \
                    board_instance.snake[tail_idx][0] - board_instance.snake[tail_idx - 1][0] == len(
                    board_instance.board) - 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[tail_idx][0] * (self.snake_size + 1) + self.snake_size / 2 + 1,
                              board_instance.snake[tail_idx][1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              self.snake_size / 2 + 1,
                              (self.snake_size / 3) * 2])
            elif board_instance.snake[tail_idx][0] - board_instance.snake[tail_idx - 1][0] == 1 or \
                    board_instance.snake[tail_idx][0] - board_instance.snake[tail_idx - 1][0] == -len(
                    board_instance.board) + 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[tail_idx][0] * (self.snake_size + 1),
                              board_instance.snake[tail_idx][1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              self.snake_size / 2 + 1,
                              (self.snake_size / 3) * 2])
            elif board_instance.snake[tail_idx][1] - board_instance.snake[tail_idx - 1][1] == 1 or \
                    board_instance.snake[tail_idx][1] - board_instance.snake[tail_idx - 1][1] == -len(
                    board_instance.board[0]) + 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[tail_idx][0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              board_instance.snake[tail_idx][1] * (self.snake_size + 1),
                              (self.snake_size / 3) * 2,
                              self.snake_size / 2 + 1])
            elif board_instance.snake[tail_idx][1] - board_instance.snake[tail_idx - 1][1] == -1 or \
                    board_instance.snake[tail_idx][1] - board_instance.snake[tail_idx - 1][1] == len(
                    board_instance.board[0]) - 1:
                pg.draw.rect(self.dis, green,
                             [board_instance.snake[tail_idx][0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                              board_instance.snake[tail_idx][1] * (self.snake_size + 1) + self.snake_size / 2 + 1,
                              (self.snake_size / 3) * 2,
                              self.snake_size / 2 + 1])

    def draw_snake(self, board_instance: board):
        for i in range(len(board_instance.snake) - 2):
            # is corner?
            pred = board_instance.snake[i]
            curr = board_instance.snake[i + 1]
            succ = board_instance.snake[i + 2]

            dx = pred[0] - succ[0]
            dy = pred[1] - succ[1]

            # is straight section
            if (abs(dx) == 2 or abs(dx) == len(board_instance.board) - 1) is not (
                    abs(dy) == 2 or abs(dy) == len(board_instance.board[0]) - 1):
                # horizontal
                if abs(dx) >= 2:
                    pg.draw.rect(self.dis, green,
                                 [curr[0] * (self.snake_size + 1) + 1,
                                  curr[1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                                  self.snake_size + 1,
                                  (self.snake_size / 3) * 2])
                elif abs(dy) >= 2:
                    pg.draw.rect(self.dis, green,
                                 [curr[0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                                  curr[1] * (self.snake_size + 1) + 1,
                                  (self.snake_size / 3) * 2,
                                  self.snake_size + 1])
            # is corner section
            else:
                pg.draw.circle(self.dis, green,
                               [curr[0] * (self.snake_size + 1) + 1 + self.snake_size / 2,
                                curr[1] * (self.snake_size + 1) + 1 + self.snake_size / 2],
                               self.snake_size / 3)

                if pred[0] < curr[0] or succ[0] < curr[0]:
                    pg.draw.rect(self.dis, green,
                                 [curr[0] * (self.snake_size + 1) + 1,
                                  curr[1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                                  self.snake_size / 2 + 1,
                                  (self.snake_size / 3) * 2])

                if pred[0] > curr[0] or succ[0] > curr[0]:
                    pg.draw.rect(self.dis, green,
                                 [curr[0] * (self.snake_size + 1) + 1 + self.snake_size / 2,
                                  curr[1] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                                  self.snake_size / 2 + 1,
                                  (self.snake_size / 3) * 2])

                if pred[1] < curr[1] or succ[1] < curr[1]:
                    pg.draw.rect(self.dis, green,
                                 [curr[0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                                  curr[1] * (self.snake_size + 1) + 1,
                                  (self.snake_size / 3) * 2,
                                  self.snake_size / 2 + 1])

                if pred[1] > curr[1] or succ[1] > curr[1]:
                    pg.draw.rect(self.dis, green,
                                 [curr[0] * (self.snake_size + 1) + self.snake_size / 6 + 1,
                                  curr[1] * (self.snake_size + 1) + 1 + self.snake_size / 2,
                                  (self.snake_size / 3) * 2,
                                  self.snake_size / 2 + 1])

    def draw_planned(self, route: list[(int, int)]):
        for (x, y) in route:
            pg.draw.rect(self.dis, bright_red,
                         [x * (self.snake_size + 1) + 1,
                          y * (self.snake_size + 1) + 1,
                         self.snake_size,
                         self.snake_size])
