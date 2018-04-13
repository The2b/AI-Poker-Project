#!/usr/bin/python3

from HandScanner import HandScanner
from Board import Board, Stage
import Card

scanner = HandScanner();
board = Board();
hands = [];

for n in range(10):
    deck = board.getDeck();

    board.setStage(Stage.RIVER_BETTING_ROUND);
    cardList = deck.dealCards(2);
    hands.append(cardList);

print(board.getPool());
winnerIndex = scanner.declareWinner(hands, board);
print("Winner index:",winnerIndex);
