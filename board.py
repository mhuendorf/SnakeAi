from enum import Enum
from random import randrange

import board


class CellType(Enum):
    EMPTY = 0
    SNAKE = 1
    APPLE = 2


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Board:

    def __init__(self, width: int, height: int, init_pos: (int, int)):

        # initialize empty board
        self.board = []
        for x in range(width):
            self.board.append([])
            for y in range(height):
                self.board[x].append(CellType.EMPTY)

        # set snake.py
        self.board[init_pos[0]][init_pos[1]] = CellType.SNAKE
        self.snake = []
        self.snake.append(init_pos)
        self.spawn_apple()

    def spawn_apple(self) -> bool:
        # get random location for the apple
        num_cells = len(self.board) * len(self.board[0])
        free_cells = num_cells - len(self.snake)
        print("free cells: {}".format(free_cells))
        if free_cells == 0:
            return False
        spawn = randrange(free_cells)

        # set the apple
        free_cells_counter = 0
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == CellType.EMPTY:
                    if free_cells_counter == spawn:
                        self.board[x][y] = CellType.APPLE
                        print("x: {}, y: {}".format(x, y))
                        break
                    elif free_cells_counter < spawn:
                        free_cells_counter += 1
                        continue
                    else:
                        raise Exception("should not be in this state")
            else:
                continue
            break
        return True

    def move(self, direction: Direction) -> bool:
        dx = 0
        dy = 0
        if direction == Direction.LEFT:
            dx = -1
        elif direction == Direction.RIGHT:
            dx = 1
        elif direction == Direction.UP:
            dy = -1
        elif direction == Direction.DOWN:
            dy = 1
        new_head_x = self.snake[0][0] + dx
        new_head_x %= len(self.board)
        new_head_y = self.snake[0][1] + dy
        new_head_y %= len(self.board[0])

        # if out of bounds
        if (new_head_x or new_head_y) < 0 or new_head_x > len(self.board) or new_head_y > len(self.board[new_head_x]):
            print("out of bounds")
            return False
        elif self.board[new_head_x][new_head_y] == CellType.SNAKE:
            if not (self.snake[len(self.snake)-1][0] == new_head_x and self.snake[len(self.snake)-1][1] == new_head_y):
                print("collided")
                return False
            else:
                self.snake.insert(0, (new_head_x, new_head_y))
                self.snake.pop()
                return True
        elif self.board[new_head_x][new_head_y] == CellType.APPLE:
            self.snake.insert(0, (new_head_x, new_head_y))
            self.board[new_head_x][new_head_y] = CellType.SNAKE
            print("yummy")
            return self.spawn_apple()
        elif self.board[new_head_x][new_head_y] == CellType.EMPTY:
            self.snake.insert(0, (new_head_x, new_head_y))
            tail_pos = self.snake.pop()
            self.board[tail_pos[0]][tail_pos[1]] = CellType.EMPTY
            self.board[new_head_x][new_head_y] = CellType.SNAKE
            return True
        else:
            raise Exception("unknown CellType")
