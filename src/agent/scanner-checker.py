#!/usr/bin/python3

from handScanner import HandScanner
from board import Board, Stage
import card

scanner = HandScanner();
board = Board();
deck = board.getDeck();

board.setStage(Stage.RIVER_BETTING_ROUND);

cardList = deck.dealCards(2, board.getDiscard());
for card in board.getPool():
    cardList.append(card);

print("Card list: ", [card.getCardID().name for card in cardList]);

bestHand = scanner.checkBestHand(cardList);

print("Best hand: ", bestHand.name);
