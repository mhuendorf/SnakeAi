from board import Direction
from board import board


def ai(playground: board, route: list[(int, int)]) -> Direction:
    if len(route) == 0:
        return None
    pos = playground.snake[0]
    dx = pos[0] - route[0][0]
    dy = pos[1] - route[0][1]
    goto = None
    # print("pos: {}, dx: {}, dy: {}".format(pos, dx, dy))
    if dx == -1 or dx == len(playground.board) - 1:
        goto = Direction.RIGHT
        #print("go right")
    elif dx == 1 or dx == -len(playground.board) + 1:
        goto = Direction.LEFT
        #print("go left")
    elif dy == -1 or dy == len(playground.board[0])-1:
        goto = Direction.DOWN
        #print("go down")
    elif dy == 1 or dy == -len(playground.board[0])+1:
        goto = Direction.UP
        #print("go up")
    return goto

# def check_feasibility(playground: board, route: list[(int, int)]) -> bool:
#     checked = []