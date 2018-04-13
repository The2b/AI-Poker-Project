'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 17 February 2018
@project Texas Hold'em AI
@file Board.py

This file will hold a class, called Board. This class will contain all the info in a more clear way on the Board,

This will make it more clear what's what than a list, as well as easier for other stuff to handle.

This will NOT handle events such as revealing new cards to agents
'''

from enum import Enum, unique # Duh
from Deck import Card, Deck # Card

class Stage(Enum):
    # Since these stages are the only time we take action, they're the only ones we'll include for now
    FIRST_BETTING_ROUND = 0;
    FLOP_BETTING_ROUND = 1;
    TURN_BETTING_ROUND = 2;
    RIVER_BETTING_ROUND = 3;
    SHOWDOWN = 4;

    def nextStage(self):
        return Stage(self.value + 1);
        

class Board:
    __NUM_CARDS_IN_HAND = 2;
    __TOTAL_CARDS_ON_BOARD = 5;

    __NUM_CARDS_PER_DECK = 52; # Should never change
    __NUM_DECKS = 1;
    __CARDS_ON_BOARD = [0,3,4,5,5];

    __stage = Stage.FIRST_BETTING_ROUND;

    __deck = Deck(__NUM_CARDS_PER_DECK,__NUM_DECKS);
    __discardPile = [];
    
    # All pool cards are pre-delt
    __flop = [];
    __turn = None;
    __river = None;

    # Money vars
    __pot = 0;
    __totalBet = 0;

    '''
    Deal all cards onto the Board
    Burning cards just to emulate the game as closely as possible.

    @param Card[] cardList
    '''
    def __init__(self): # @TODO May want to change it to require a deck, since we'll need to use the same deck to deal out agent's hands.
        self.__deck.resetDeck();

        # Burn 1
        #self.__deck.dealCard();

        # Turn 3
        self.__flop = self.__deck.dealCards(3);

        # Burn
        #self.__deck.dealCard();

        # Turn
        self.__turn = self.__deck.dealCard();

        # Burn
        #self.__deck.dealCard();

        # Turn
        self.__river = self.__deck.dealCard();

    def getStage(self):
        return self.__stage;

    def setStage(self, stageID):
        self.__stage = stageID;
        return;

    def getCardsOnBoard(self):
        return self.__CARDS_ON_BOARD[self.getStage().value];

    def getFlop(self):
        if(self.getStage().value > Stage.FIRST_BETTING_ROUND.value): # if currStage is after the first betting round...
            return self.__flop;
        return None;

    def getTurn(self):
        if(self.getStage().value > Stage.FLOP_BETTING_ROUND.value): 
            return self.__turn;
        return None;

    def getRiver(self):
        if(self.getStage().value > Stage.TURN_BETTING_ROUND.value):
            return self.__river;
        return None;

    def getPool(self):
        cards = [];
        flop = self.getFlop();
        if(not flop):
            return cards;
        
        turn = self.getTurn();
        if(not turn):
            return flop;

        river = self.getRiver();

        for index in flop:
            cards.append(index);

        if(turn):
            cards.append(turn);

        if(river):
            cards.append(river);

        return cards;

    def getCardsPerHand(self):
        return self.__NUM_CARDS_IN_HAND;

    def getTotalCardsOnBoard(self):
        return self.__TOTAL_CARDS_ON_BOARD;

    def getDeck(self): # As far as I know, this is for testing purposes, and should not be public in production. @TODO
        return self.__deck;

    def getPot(self):
        return self.__pot;

    def getBet(self):
        return self.__totalBet;

    def setPot(self, money):
        self.__pot = money;
        return;

    def addToPot(self, money):
        self.__pot += money;
        return;

    def setBet(self, bet):
        self.__totalBet = bet;
        return;

    def addToBet(self, betToAdd):
        self.__totalBet += betToAdd;
        return;
