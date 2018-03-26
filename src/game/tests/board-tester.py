#!/usr/bin/python3

from Board import Board, Stage

board = Board();

for index in Stage:
    board.setStage(index);
    print("Index Value: ",index.value);
    print("Stage: ",board.getStage());
    print("Pool: ",board.getPool());
    print("DisCard: ",board.getDisCard());
    print("Deck: ", board.getDeck());
