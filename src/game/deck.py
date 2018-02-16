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

 @NOTE I'm currently making the card class, among other things which will be split into different files later. I'm doing it here for my convenience, so try to avoid importing these until that's done.
 '''

from enum import Enum, unique
import sys, copy, os, math

@unique
class CardIDs(Enum):
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

class Card(int idNum):
    int __cardID = 0; # Must be init'd, or it'll be super inconsistent on calls. Uses the CardIDs enum above. Wraps on overflow, not on underflow
    
    __init__(self):
        if(idNum > 52):
            __cardID = idNum % 52;
        else if(idNum < 0):
            print("ERROR: Requested card ID is less than 0; exiting");
            sys.exit(0101);        



class Deck(int cardsPerDeck, int deckCount):

    # Varible declaration; Default to a single 52 card deck
    int __numCardsPerDeck = 52;
    int __numDecks = 1;

    Card __cards[] = {};

    def __init__(self, cardsPerDeck, deckCount):
            __setCardsPerDeck(cardsPerDeck);
            __setNumDecks(deckCount);

            for(int dIndex = 0; i < __numDecks; index++): # For each deck, add 52 cards to the deck array
              for(int cIndex = 0; i < __numCardsPerDeck; index++):
                    __cards.append(Card(index+1);

            

    def getCardsPerDeck(self):
        return self.__numCardsPerDeck;

    def getNumDecks(self):
        return self.__numDecks;

    def getCards(self):
        return self.__cards;

    # ONLY use this for __init__
    def __setCardsPerDeck(self, int cardNum):
        if(cardNum == None): # This is for __init__, to clean it up. Basically does what we would do in init. This needs to be first so we can save a few cycles checking if the values are None twice per change
            return;

        if(cardNum > 52 || cardNum < 1):
            printf("Invalid value for cards per deck, %d. Not going to touch it", cardNum);
            return;

        self.__cardsPerDeck = cardNum;
        return;

    def __setNumDecks(self, int deckCount):
        if(deckCount == None): # Same reason as above
            return;

        if(deckCount < 1):
            print("Invalid value for number of decks, %d. Not going to touch it", deckCount);
            return;
            
        self.__numDecks = deckCount;
        return;

    def dealCard(self, Card discard[]):
        '''
        Clone the __cards array, subtract the discard pile, RNG a value
        Also, we can overload this with no arguments to just RNG a card out of the array

        I'm leaving that second line in, but fuck python for not allowing overloading
        '''

        Card cardsDup[] = copy.deepcopy(self.getCards());
        if(discard != None):
            cardsDup -= discard;

        Card rngCard = cardsDup[os.urandom % cardsDup.len()];

        return rngCard;

    def dealCards(self, int numCards, Card discardPile[]):
        '''
        Return an array of numCards random cards. Use a discard array to avoid dup's
        Using this, we can deal out ((2*numPlayers)+5) cards in order, and classify them after
        '''
        int cardsDelt[] = {};
        int discard[] = discardPile; # So we can affect the discard pile appropriately
        int cardsDup[] = copy.deepcopy(self.getCards());

        for(int index = 0; index < numCards; index++):
            # Remove all the already used cards
            cardsDup -= discard;
            
            '''
            I don't want to use os.random since I don't know how many numbers need to be generated,
            and don't want the program to lock up waiting in an uninterruptable sleep waiting for
            entropy that won't be generated. If I notice issues with RNG (which I almost certainly won't, cuz human), I'll change it

            I also want to use the cardsDelt length instead of anything using the cards per deck and number of decks
            since it'll be ugly to incorporate all that and the discard array, which I'd need to call the size of anyway.
            So why do the extra calcs? Verification isn't super important, given the inconsistent nature of the sising of arrays.
            '''
            Card rngCard = cardsDup[os.urandom % cardsDelt.len()]; # Generate a random card; Doing this here so I can add it to the discard pile as well 
            cardsDelt.append(rngCard);
            discard.append(rngCard);

        return cardsDelt; # No need to do anything w/ discard; Because of how it was declared locally, all changes will be made; Effecitvely passed by reference

    def resetDeck(self):
        self.__init__(None,None);
