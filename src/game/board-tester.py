#!/usr/bin/python3

from board import Board, Stage
import random

board = Board();

for index in Stage:
    board.setStage(index);
    print(board.getPool());
    print("Discard: ",board.getDiscard());
    print("Deck: ", board.getDeck());
