#!/usr/bin/python3

'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 12 March 2018
@project Texas Hold'em AI
@file HandOddsWorkerFunctions.py
'''

'''
Will hold the functions for the generators to parallelize
'''

from HandScanner import HandScanner, HandIDs
from Board import Board, Stage
from Card import Card
from Deck import Deck

import multiprocessing as mp

__NUM_HANDS = 10;
__TIMEOUT = 2;

def playSet(batchsize,queue):
    while(True):
        #print("Playing set...");

        for i in range(batchsize):
            queue.put(playHand(), timeout=__TIMEOUT);
    return;

def playHand():
    scanner = HandScanner();
    board = Board();
    deck = board.getDeck();

    board.setStage(Stage.RIVER_BETTING_ROUND);
    deck.resetDeck();

    cardList = deck.dealCards(2);

    for card in board.getPool():
        cardList.append(card);
   
    #print([card.getCardID().name for card in cardList]);
    
    bestHand = scanner.checkBestHand(cardList);

    #print("Best hand: ", bestHand.name);

    return bestHand;
