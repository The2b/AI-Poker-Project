#!/usr/bin/python3

from board import Board, Stage

board = Board();

for index in Stage:
    board.setStage(index);
    print("Index Value: ",index.value);
    print("Stage: ",board.getStage());
    print("Pool: ",board.getPool());
    print("Discard: ",board.getDiscard());
    print("Deck: ", board.getDeck());
