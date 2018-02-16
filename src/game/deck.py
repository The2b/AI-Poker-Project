#!/usr/bin/python3

# @author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
# @date 15 Feb 2018
# @project AI-Texas-Holdem
# @file deck.py

'''
 The purpose of this file is to enumerate the deck and manage a discard pile, as well as add methods for things such as dealing.
 This may change to just be an enumeration file, and have a seperate controller class
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

from enum import Enum, unique

@unique
class Deck(Enum):
    # Spades
    ACE_OF_SPADES = 1;
    TWO_OF_SPADES = 2;
    THREE_OF_SPADES = 3;
    FOUR_OF_SPADES = 4;
    FIVE_OF_SPADES = 5;
    SIX_OF_SPADES = 6;
    SEVEN_OF_SPADES = 7;
    EIGHT_OF_SPADES = 8;
    NINE_OF_SPADES = 9;
    TEN_OF_SPADES = 10;
    JACK_OF_SPADES = 11;
    QUEEN_OF_SPADES = 12;
    KING_OF_SPADES = 13;

    # Clubs
    ACE_OF_CLUBS = 14;
    TWO_OF_CLUBS = 15;
    THREE_OF_CLUBS = 16;
    FOUR_OF_CLUBS = 17;
    FIVE_OF_CLUBS = 18;
    SIX_OF_CLUBS = 19;
    SEVEN_OF_CLUBS = 20;
    EIGHT_OF_CLUBS = 21;
    NINE_OF_CLUBS = 22;
    TEN_OF_CLUBS = 23;
    JACK_OF_CLUBS = 24;
    QUEEN_OF_CLUBS = 25;
    KING_OF_CLUBS = 26;

    # Hearts
    ACE_OF_HEARTS = 27;
    TWO_OF_HEARTS = 28;
    THREE_OF_HEARTS = 29;
    FOUR_OF_HEARTS = 30;
    FIVE_OF_HEARTS = 31;
    SIX_OF_HEARTS = 32;
    SEVEN_OF_HEARTS = 33;
    EIGHT_OF_HEARTS = 34;
    NINE_OF_HEARTS = 35;
    TEN_OF_HEARTS = 36;
    JACK_OF_HEARTS = 37;
    QUEEN_OF_HEARTS = 38;
    KING_OF_HEARTS = 39;

    # Diamonds
    ACE_OF_DIAMONDS = 40;
    TWO_OF_DIAMONDS = 41;
    THREE_OF_DIAMONDS = 42;
    FOUR_OF_DIAMONDS = 43;
    FIVE_OF_DIAMONDS = 44;
    SIX_OF_DIAMONDS = 45;
    SEVEN_OF_DIAMONDS = 46;
    EIGHT_OF_DIAMONDS = 47;
    NINE_OF_DIAMONDS = 48;
    TEN_OF_DIAMONDS = 49;
    JACK_OF_DIAMONDS = 50;
    QUEEN_OF_DIAMONDS = 51;
    KING_OF_DIAMONDS = 52;

    '''Use this method to get the numerical value of a card

    @param int card
    @return int numValue
    '''
    def getCardNum(int card):
        # Modulo 13 to remove the suit multiplier
        int val = card % 13;
        return val;

    def getCardSuit(int card):
        # Store the modulo 13 and subtract it, removing the numerical value
        int numVal = card % 13;
        int suit = card - numVal;
        # Then divide it, which will always be an int thanks to modulo, giving the suit multiplier
        suit = suit / 13;
        return Suits.suit;

@unique
class Suits(Enum):
    SPADES = 0;
    CLUBS = 1;
    HEARTS = 2;
    DIAMONDS = 3;
