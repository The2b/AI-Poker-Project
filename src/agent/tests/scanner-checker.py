#!/usr/bin/python3

from HandScanner import HandScanner
from Board import Board, Stage
import Card

scanner = HandScanner();

for n in range(10):
    board = Board();
    deck = board.getDeck();

    board.setStage(Stage.RIVER_BETTING_ROUND);

    cardList = deck.dealCards(2);
    for card in board.getPool():
        cardList.append(card);

    print("Card list: ", [card.getCardID().name for card in cardList]);

    bestHand = scanner.checkBestHand(cardList);

    print("Best hand: ", bestHand.name);
