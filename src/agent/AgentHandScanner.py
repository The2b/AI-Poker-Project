'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 22 February 2018
@project Texas Hold'em AI
@file AgentHandScanner.py

This is where I'm going to keep the functions to see what we have in our hand
'''

from deck import Card

class AgentHandScanner:

    '''
    Checks the parent agent's hand and the board to see if we have a pair in our hand.
    Does **NOT** calculate odds. It does, however, verify there are enough cards to form a hand before it checks anything.

    @param Card cards[]
    @return boolean hasPair
    '''
    def checkPair(self, cards):

    '''
    Checks if the parents cards has 2 pairs

    @param Card cards[]
    @return boolean hasTwoPair
    '''
    def checkTwoPair(self, cards):

    '''
    Checks if the parents cards have a 3 of a kind

    @param Card cards[]
    @return boolean hasThreeOfAKind
    '''
    def checkThreeOfAKind(self, cards):

    '''
    Checks if the parents cards have a straight

    @param Card cards[]
    @return boolean hasStraight
    '''
    def checkStraight(self, cards):

    '''
    Checks if the parents cards have a flush

    @param Card cards[]
    @return boolean hasStraight
    '''
    def checkFlush(self, cards):

    '''

    '''
    def checkFullHouse(self, cards):

    '''

    '''
    def checkFourOfAKind(self, cards):

    '''
    
    '''
    def checkStraightFlush(self, cards):

