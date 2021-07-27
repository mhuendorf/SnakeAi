import time

import pygame as pg
import random
import renderer as rnd
import board as brd
from ai import ai

BOARD_SIZE_X = 20
BOARD_SIZE_Y = 20
SNAKE_BLOCK_SIZE = 20


def game_loop(renderer: rnd.Renderer, board: brd.Board):
    clock = pg.time.Clock()
    snake_speed = 10
    game_over = False
    quit_game = False
    pause = False
    counter = 0
    last_direction = brd.Direction.RIGHT
    # pick a font you have and set its size
    #myfont = pg.font.SysFont("Comic Sans MS", int(SNAKE_BLOCK_SIZE * BOARD_SIZE_X / 6))
    # apply it to text on a label
    #label = myfont.render("Game Over!", 1, (50, 0, 0))
    route = []
    while not (quit_game or game_over):
        if len(route) == 0:
            route = board.wave_front()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and not pause:
                    last_direction = change_direction(last_direction, brd.Direction.LEFT)
                elif event.key == pg.K_RIGHT and not pause:
                    last_direction = change_direction(last_direction, brd.Direction.RIGHT)
                elif event.key == pg.K_SPACE:
                    pause = not pause
        if not pause:
            new_direction = ai(board, route)
            if len(route) != 0:
                route.pop(0)
            if new_direction is not None:
                last_direction = new_direction
            else:
                print("müll")
            if not board.move(last_direction):
                pause = True
            renderer.render_scene(board, route)
            pg.display.update()
            counter += 1
        clock.tick(snake_speed)
    if (game_over):
        # put the label object on the screen at point x=100, y=100
        #renderer.dis.blit(label, (0, 0))
        pg.display.update()
        time.sleep(2)
    pg.quit()
    quit()


def change_direction(to_change: brd.Direction, direction: brd.Direction) -> brd.Direction:
    if direction == brd.Direction.RIGHT:
        if to_change == brd.Direction.LEFT:
            return brd.Direction.UP
        if to_change == brd.Direction.UP:
            return brd.Direction.RIGHT
        if to_change == brd.Direction.RIGHT:
            return brd.Direction.DOWN
        if to_change == brd.Direction.DOWN:
            return brd.Direction.LEFT
    else:
        if to_change == brd.Direction.LEFT:
            return brd.Direction.DOWN
        if to_change == brd.Direction.UP:
            return brd.Direction.LEFT
        if to_change == brd.Direction.RIGHT:
            return brd.Direction.UP
        if to_change == brd.Direction.DOWN:
            return brd.Direction.RIGHT


if __name__ == "__main__":
    renderer = rnd.Renderer(BOARD_SIZE_X, BOARD_SIZE_Y, SNAKE_BLOCK_SIZE)
    board = brd.Board(BOARD_SIZE_X, BOARD_SIZE_Y, (int(BOARD_SIZE_X/2-1), int(BOARD_SIZE_Y/2-1)))
    game_loop(renderer, board)