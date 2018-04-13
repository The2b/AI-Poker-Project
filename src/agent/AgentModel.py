'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 26 March 2018
@project Texas Hold'em AI
@file AgentModel.py
'''

from HandScanner import HandScanner

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

    def __init__(self):
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

        self.__hand = [];
        self.inGame = True;

    def resetAgent(self):
        self.__init__();

    def getHand(self):
        return self.__hand;

    def setHand(self, newHand):
        self.__hand = newHand;
        return;
