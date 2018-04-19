#!/usr/bin/python3

from Board import Board, Stage

board = Board();

for stage in Stage:
    print(type(stage));
    board.setStage(stage);
    print("Index Value: ",stage.value);
    print("Stage: ",board.getStage());
    print("Pool: ",board.getPool());
    print("Deck: ", board.getDeck());
