#!/usr/bin/python3

from HandScanner import HandScanner
from Board import Board, Stage
import Card

scanner = HandScanner();
board = Board();
deck = board.getDeck();


for n in range(10):
    board.setStage(Stage.RIVER_BETTING_ROUND);

    cardList = deck.dealCards(2);
    for card in board.getPool():
        cardList.append(card);

    print(len(deck.getCards()),len(board.getDeck().getCards()));

    print("Card list: ", [card.getCardID().name for card in cardList]);

    bestHand = scanner.checkBestHand(cardList);

    print("Best hand: ", bestHand.name);
