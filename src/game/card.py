#!/usr/bin/python3

'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 22 Feb 2018
@project Texas Hold'em AI
@file card.py
@ErrorID 1XX
'''

'''
 The purpose of this file is to enumerate the cards, and give them functions for proper, controlled access
 I'm going to do it by suit since that's easier for me to conceptualize, but that may also change later

 
 As it stands, each value can be accessed with the following algorithm:
    (SuitMult * 13) + Value

 With Value being the value of the card (Jack = 11, Queen = 12, King = 13, Ace = 1)
 SuitMult:
    Spades = 0
    Clubs = 1
    Hearts = 2
    Diamonds = 3

 They can also be accessed by their name, in the form
    <CARD_NAME>_OF_<SUIT>

 Where CARD_NAME is the number of the card, or title for face cards and aces
 Suit is the name of the suit, in all caps, as defined statically below.
'''

'''
Error Codes:
    101: Requesting a card with an ID less than 0. This crashes the program, since this must be a corruption issue atm
'''

from enum import Enum, unique # Duh
import sys # exit
import copy # deepcopy
import random # randint
import operator # sub

@unique
class CardIDs(Enum):
    # Spades
    ACE_OF_SPADES = 0;
    TWO_OF_SPADES = 1;
    THREE_OF_SPADES = 2;
    FOUR_OF_SPADES = 3;
    FIVE_OF_SPADES = 4;
    SIX_OF_SPADES = 5;
    SEVEN_OF_SPADES = 6;
    EIGHT_OF_SPADES = 7;
    NINE_OF_SPADES = 8;
    TEN_OF_SPADES = 9;
    JACK_OF_SPADES = 10;
    QUEEN_OF_SPADES = 11;
    KING_OF_SPADES = 12;

    # Clubs
    ACE_OF_CLUBS = 13;
    TWO_OF_CLUBS = 14;
    THREE_OF_CLUBS = 15;
    FOUR_OF_CLUBS = 16;
    FIVE_OF_CLUBS = 17;
    SIX_OF_CLUBS = 18;
    SEVEN_OF_CLUBS = 19;
    EIGHT_OF_CLUBS = 20;
    NINE_OF_CLUBS = 21;
    TEN_OF_CLUBS = 22;
    JACK_OF_CLUBS = 23;
    QUEEN_OF_CLUBS = 24;
    KING_OF_CLUBS = 25;

    # Hearts
    ACE_OF_HEARTS = 26;
    TWO_OF_HEARTS = 27;
    THREE_OF_HEARTS = 28;
    FOUR_OF_HEARTS = 29;
    FIVE_OF_HEARTS = 30;
    SIX_OF_HEARTS = 31;
    SEVEN_OF_HEARTS = 32;
    EIGHT_OF_HEARTS = 33;
    NINE_OF_HEARTS = 34;
    TEN_OF_HEARTS = 35;
    JACK_OF_HEARTS = 36;
    QUEEN_OF_HEARTS = 37;
    KING_OF_HEARTS = 38;

    # Diamonds
    ACE_OF_DIAMONDS = 39;
    TWO_OF_DIAMONDS = 40;
    THREE_OF_DIAMONDS = 41;
    FOUR_OF_DIAMONDS = 42;
    FIVE_OF_DIAMONDS = 43;
    SIX_OF_DIAMONDS = 44;
    SEVEN_OF_DIAMONDS = 45;
    EIGHT_OF_DIAMONDS = 46;
    NINE_OF_DIAMONDS = 47;
    TEN_OF_DIAMONDS = 48;
    JACK_OF_DIAMONDS = 49;
    QUEEN_OF_DIAMONDS = 50;
    KING_OF_DIAMONDS = 51;


@unique
class Suits(Enum):
    SPADES = 0;
    CLUBS = 1;
    HEARTS = 2;
    DIAMONDS = 3;

class Card:
    __cardID = -1; # Must be init'd, or it'll be super inconsistent on calls. Uses the CardIDs enum above. Wraps on overflow, not on underflow
    __cardNum = 0; # Must be init'd. Stored so we don't waste time on a bunch of division
    __cardSuit = -1; # Same as above
    
    '''
    Create a Card object. Init's card values based on the given ID.
    If an ID is greater than 52, modulo it by 52. TBH this is a week later and I don't know why I chose
        that method to handle errors. But I'm sure I had a reason. I REMEMBERED!!! It's so that if we have multiple decks, it'll be handled correctly.
    If the given ID is less than 1, error out

    @param int>0 idNum
    '''
    def __init__(self, idNum):
        if(idNum >= 52):
            idNum = idNum % 52;
        elif(idNum < 0):
            print("ERROR: Requested card ID is less than 0; exiting"); # @TODO I may want to change this to check for less than 1 instead, since I don't have a card defined for 0 as is. It's just as bad as having a threshold at -1, really
            sys.exit(101);        

        self.__cardID = CardIDs(idNum);
        self.__cardNum = self.__calcCardNum();
        self.__cardSuit = self.__calcCardSuit();

        #print("Card ID: ", self.getCardID()); # @DEBUG
        #print("Card Num: ", self.getCardNum()); # @DEBUG
        #print("Suit: ", self.getCardSuit()); # @DEBUG


    '''
    Use this method to get the numerical value of a card. Because division is hard, I'm going to assign this to a value and use that instead

    @param int card
    @return int numValue
    '''
    def __calcCardNum(self):
        # Modulo 13 to remove the suit multiplier
        val = self.getCardID().value % 13;
        return val+1;

    '''
    Takes the int id and returns the suit of the card. Same division thing as above

    @param cardID
    @return suitID
    '''
    def __calcCardSuit(self):
        # Store the modulo 13 and subtract it, removing the numerical value
        numVal = self.getCardNum();
        suit = self.getCardID().value - (numVal-1);
        # Then divide it, which will always be an int thanks to modulo, giving the suit multiplier
        suit = suit / 13;
        return Suits(suit);

    '''
    The function for the outside world to pull the card ID. This will pull the enumerated name, not value

    @return CardIDs cardID
    '''
    def getCardID(self):
        return self.__cardID;
        
    '''
    The function for the outside world to pull the card's numerical value. This will pull an int

    @return int ___cardNum
    '''
    def getCardNum(self):
        return self.__cardNum;

    '''
    The function for the outside world to pull the card's suit. This will pull the enumerated name, not value
    
    @return Suits __cardSuit
    '''
    def getCardSuit(self):
        return Suits(self.__cardSuit);
