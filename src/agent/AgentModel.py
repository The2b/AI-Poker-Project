'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 26 March 2018
@project Texas Hold'em AI
@file AgentModel.py
'''

from HandScanner import HandScanner
from NeuralNet import NeuralNet
import pdb

class AgentModel:
    # Flags on what hands we have at the moment
    hasHighCard = False;
    hasPair = False;
    hasTwoPair = False;
    hasThree = False;
    hasStraight = False;
    hasFlush = False;
    hasFullHouse = False;
    hasFour = False;
    hasStraightFlush = False;
    hasFive = False;

    numPairs = 0; # This is particularly helpful for three and four of a kind, when we need to worry about how many of our cards are paired
    numThrees = 0; # Same as above, but for three of a kinds. No need for one for four because we can't have 8 cards

    # Flags on what hands are impossible to get
    zeroHighCard = False;
    zeroPair = False;
    zeroTwoPair = False;
    zeroThree = False;
    zeroStraight = False;
    zeroFlush = False;
    zeroFullHouse = False;
    zeroFour = False;
    zeroStraightFlush = False;
    zeroFive = False;

    # Flags to check if an agent is in the game. This should be changed for all agents at the start of each hand
    inGame = False;

    __hand = [];

    cash = 0;
    inPot = 0;
    inPotThisRound = 0;

    oppoModel = 0;

    def __init__(self, quiet=True, build=True):
        '''
        self.hasHighCard = False;
        self.hasPair = False;
        self.hasTwoPair = False;
        self.hasThree = False;
        self.hasStraight = False;
        self.hasFlush = False;
        self.hasFullHouse = False;
        self.hasFour = False;
        self.hasStraightFlush = False;
        self.hasFive = False;

        self.numPairs = 0;
        self.numThrees = 0;

        self.zeroHighCard = False;
        self.zeroPair = False;
        self.zeroTwoPair = False;
        self.zeroThree = False;
        self.zeroStraight = False;
        self.zeroFlush = False;
        self.zeroFullHouse = False;
        self.zeroFour = False;
        self.zeroStraightFlush = False;
        self.zeroFive = False;
        '''

        self.__hand = [];
        self.inGame = True;

        if(build):
            self.oppoModel = NeuralNet(csvPath="/home/the2b/Documents/school/ai/project/src/temp.csv", dataUrl = "/home/the2b/Documents/school/ai/project/src/temp.csv", quiet=quiet);
            #self.oppoModel = NeuralNet(quiet=quiet);

    def resetAgent(self):
        self.__init__(build=False);

    def getHand(self):
        return self.__hand;

    def getCash(self):
        return self.cash;

    def getCashInPot(self):
        return self.inPot;

    def setCash(self, cash):
        self.cash += cash;
        return;

    def setCashInPot(self, cash):
        self.inPot = cash;
        return;

    def resetCashInPotThisRound(self):
        self.setCashInPotThisRound(0);
        return;

    def getCashInPotThisRound(self):
        return self.inPotThisRound;

    def setCashInPotThisRound(self, cash):
        self.inPotThisRound = cash;
        return;

    def addToCashInPot(self, board, cashToAdd):
        if(self.cash < cashToAdd):
            print("Agent has insufficient funds");
            self.inPot += self.cash;
            self.inPotThisRound += self.cash;
            board.addToPot(self.cash);
            self.removeCash(self.cash);

        self.inPot += cashToAdd;
        self.inPotThisRound += cashToAdd;
        board.addToPot(cashToAdd);
        self.removeCash(cashToAdd);
        return True;

    def addCash(self, cashToAdd):
        self.cash += int(cashToAdd);
        return;

    def removeCash(self, cashToRemove):
        if(self.cash < cashToRemove):
            print("Agent has insufficient funds. Setting to 0");
            self.setCash(0);
            return;
        self.cash -= cashToRemove;
        return;

    def setHand(self, newHand):
        self.__hand = newHand;
        return;
