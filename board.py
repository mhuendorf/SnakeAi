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
        self.snake = []
        for x in range(width):
            self.board.append([])
            for y in range(height):
                self.board[x].append(CellType.EMPTY)

        # set snake.py
        self.board[init_pos[0]][init_pos[1]] = CellType.SNAKE
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
            if not (self.snake[len(self.snake) - 1][0] == new_head_x and self.snake[len(self.snake) - 1][
                1] == new_head_y):
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

    def get_neighbors(self, x: int, y: int) -> list[tuple]:
        width = len(self.board)
        height = len(self.board[1])
        x = x + width
        y = y + height
        neighbors = []
        neighbors.extend([((x - 1) % width, y % height),
                          (x % width, (y - 1) % height),
                          ((x + 1) % width, y % height),
                          (x % width, (y + 1) % height)])
        return neighbors

    def wave_front(self):
        board_values = []
        for x in range(len(self.board)):
            board_values.append([])
            for y in range(len(self.board[x])):
                board_values[x].append(len(self.board)*len(self.board[0])+1)

        for i in range(len(self.snake)):
            board_values[self.snake[i][0]][self.snake[i][1]] = i - len(self.snake)

        s = (self.snake[0][0], self.snake[0][1], 0)
        board_values[self.snake[0][0]][self.snake[0][1]] = 0
        queue = [s]
        apple_found = False
        apple = (-1, -1, -1)
        while len(queue) > 0:
            active_node = queue.pop()
            level = active_node[2]
            for node in self.get_neighbors(active_node[0], active_node[1]):
                #print(node, level)
                if board_values[node[0]][node[1]] == len(self.board)*len(self.board[0])+1 and self.board[node[0]][node[1]] != CellType.SNAKE:
                    board_values[node[0]][node[1]] = level + 1
                    if not apple_found:
                        if self.board[node[0]][node[1]] == CellType.EMPTY:
                            queue.insert(0, (node[0], node[1], level+1))
                        else:
                            apple_found = True
                            apple = (node[0], node[1], level+1)
                elif self.board[node[0]][node[1]] == CellType.SNAKE and board_values[node[0]][node[1]] < 0 and board_values[node[0]][node[1]] + level + 1 >= 0:
                    board_values[node[0]][node[1]] = level + 1
                    queue.insert(0, (node[0], node[1], level + 1))

        for y in range(len(self.board[0])):
            for x in range(len(self.board)):
                print("{:4d}".format(board_values[x][y]), end=" ")
            print()

        route_constructed = apple[2] == 1
        curr_node = apple
        route = [(apple[0], apple[1])]
        while not route_constructed:
            for neighbor in self.get_neighbors(curr_node[0], curr_node[1]):
                if curr_node[2] > board_values[neighbor[0]][neighbor[1]] >= 0:
                    route.insert(0, neighbor)
                    curr_node = (neighbor[0], neighbor[1], board_values[neighbor[0]][neighbor[1]])
                    if board_values[neighbor[0]][neighbor[1]] == 1:
                        route_constructed = True
                    break
            else:
                return []
        return route
