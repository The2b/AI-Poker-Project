#!/usr/bin/python3

'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 15 Feb 2018
@project Texas Hold'em AI
@file deck.py
@ErrorID 2XX
'''

'''
 The purpose of this class to deck management, and to give the deck functions for proper access.
 In effect, this is a portal to the cards, which are all stored in a list.
'''

from enum import Enum, unique # Duh
import sys # exit
import copy # deepcopy
import random # randint
import operator # sub
from card import Card # Duh. It shouldn't access any enumeration directly

class Deck:

    # Varible declaration; Default to a single 52 card deck
    __numCardsPerDeck = 52; # There's no real reason for this to change. But I'm leaving it here in case we find *some* use for it...
    __numDecks = 1;

    __cards = [];

    '''
    Creates the Deck object and assigns the values required to define the proper number of cards and decks.
    The handlers for null values are in the set option, and therefore can be ignored

    @param int cardsPerDeck (optional)
    @param int deckCount (optional)
    '''
    def __init__(self, cardsPerDeck, deckCount):
            self.__setCardsPerDeck(cardsPerDeck);
            self.__setNumDecks(deckCount);

            # For each deck, add __numCardsPerDeck cards to the deck array
            for dIndex in range(0, self.__numDecks):
                for cIndex in range(0, self.__numCardsPerDeck):
                    self.getCards().append(Card(cIndex+1)); # Anon objects are fine in Python, right?

            
    # Getter for __numCardsPerDeck
    def getCardsPerDeck(self):
        return self.__numCardsPerDeck;

    # Getter for __numDecks
    def getNumDecks(self):
        return self.__numDecks;

    # Getter for __cards; This one may be really useless...
    def getCards(self):
        return self.__cards;

    '''
    Pull a list of all the card IDs in the deck

    @return cardIDs[]
    '''
    def getCardIDs(self):
        cardIDs = [];
        cardList = copy.deepcopy(self.getCards());
        for index in range(0, len(cardList)):
            cardIDs.append(cardList[index].getCardID());
        return cardIDs;

    '''
    Sets the number of cards per deck. If it's over 52, it'll modulo the value. TBH this is a week after I originally wrote this
    and idk why I chose that to handle the error instead of just making it 52. But I'm sure I have a reason.

    If it's under 1, it tells you and ignores the input, returning -10

    ONLY use this for __init__
    '''

    def __setCardsPerDeck(self, cardNum):
        if(cardNum == None): # This is for __init__, to clean it up. Basically does what we would do in init. This needs to be first so we can save a few cycles checking if the values are None twice per change
            return;

        if(cardNum > 52 | cardNum < 1):
            print("Invalid value for cards per deck, ",cardNum, ". Not going to touch it");
            return;

        self.__cardsPerDeck = cardNum;
        return;

    def __setNumDecks(self, deckCount):
        if(deckCount == None): # Same reason as above
            return;

        if(deckCount < 1):
            print("Invalid value for number of decks, %d. Not going to touch it", deckCount);
            return;
            
        self.__numDecks = deckCount;
        return;

    def dealCard(self, discard):
        '''
        Clone the __cards array, subtract the discard pile, RNG a value
        Also, we can overload this with no arguments to just RNG a card out of the array

        I'm leaving that second line in, but fuck python for not allowing overloading
        '''

        cardsDup = copy.deepcopy(self.getCardIDs());
        if(discard != None):
            cardsDup = list(set(cardsDup) - set(discard)); # @TODO Make this work, at the moment cardsDup has pointers

        else:
            discard = [];

        '''
        I don't want to use os.random since I don't know how many numbers need to be generated,
        and don't want the program to lock up waiting in an uninterruptable sleep waiting for
        entropy that won't be generated. If I notice issues with RNG (which I almost certainly won't, cuz human), I'll change it

        I also want to use the cardsDelt length instead of anything using the cards per deck and number of decks
        since it'll be ugly to incorporate all that and the discard array, which I'd need to call the size of anyway.
        So why do the extra calcs? Verification isn't super important, given the inconsistent nature of the sising of arrays.
        '''

        rngCard = cardsDup[random.randint(0,len(cardsDup)-1)];

        discard.append(rngCard);

        return rngCard;

    def dealCards(self, numCards, discard):
        '''
        Return an array of numCards random cards. Use a discard array to avoid dup's
        Using this, we can deal out ((2*numPlayers)+5) cards in order, and classify them after
        '''

        # Verify we're not asking for more than 52 cards, which is impossible.
        if(numCard > 52):
            print("Trying to deal more than 52 cards, which exceeds the limit. There's no reason to ask for this many, so something error'd out. Exiting...");
            sys.exit(103);
        # If it's not defined, skip the next part
        if(discard != None):
            # Make sure we're not trying to deal more cards than we have in the deck
            if(numCards > (self.getCardsPerDeck() - len(discard))):
                print("Too many cards trying to be delt; Try shuffling and go again")
                return 102;

        else:
            discard = [];

        cardsDelt = [];

        for index in range(0, numCards):
            cardsDelt.append(self.dealCard(discard));

        return cardsDelt; # No need to do anything w/ discard; Because of how it was declared locally, all changes will be made; Effecitvely passed by reference

    def resetDeck(self):
        self.__init__(None,None);
