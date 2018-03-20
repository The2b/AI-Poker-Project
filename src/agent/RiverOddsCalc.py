'''
@author Thomas Lenz <thoams.lenz96@gmail.com> AS The2b
@date 19 March 2018
@project Texas Hold'em AI
@file RiverOddsCalc.py
'''

'''
This will handle the odds that any given hand will complete on the river. The turn-to-river calcs will be highly dependent on this.
'''

from deck import Deck
from board import Board, Stage
from card import Suits
from handScanner import HandScanner

import copy # Deepcopy

def pairRiverOdds(cards, board, agentFlags=0):
    # This method doesn't check if we already have a pair. That should be done by the agent before this.
    # First, calc some pre-req calcs
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Calc the outs per card and total outs
    outsPerCard = (board.getDeck().getNumDecks() * len(Suits) - 1);
    totalOuts = (outsPerCard * cardsShown);

    # Invert it and return it
    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def twoPairRiverOdds(cards, board, agentFlags=0):
    # Basically, the same thing as above, but two less cardsShown. This isn't going to be perfect in the first implementation, specifically if there's already a three-of-a-kind or more, but I don't really care, since this is meaningless if that's the case
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Calc the outs
    outsPerCard = (board.getDeck().getNumDecks() * len(Suits) - 1);
    totalOuts = (outsPerCard * (cardsShown - 2));

    # Invert it and return it
    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def threeRiverOdds(cards, board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Calc the outs. These ones are the same as the twoPair one, but it won't be multiplied by the cards shown to calc total outs
    outs = (board.getDeck().getNumDecks() * len(Suits) - 1);
    totalOuts = (outs); # For consistency. Don't give a damn about two cycles.

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

'''
This function is a prototype which reverts to the inner or outer straight functions, based on what's appropriate. Has its own checking, but that may be outsourced later
'''
def straightRiverOdds(cards, board, agentFlags=0):
    # Check for an outer one first. Very similar to the handScanner's straight implementation, but checking for 4 in a row instead of five
    cardNumsFirst = [card.getCardNum() for card in cards];
    cardNumsSet = set(cardNumsFirst);
    cardNums = list(cardNumsSet);
    cardNums.sort();
    counter = 1;
    NUM_ACE_HIGH = 14;
    NUM_ACE_LOW = 1;

    # Check for outer straights
    for index in range(1,len(cardNums)):
        if(cardNums[index] == cardNums[index-1] + 1):
            counter += 1;
            if(counter >= 4):
                return outerStraightRiverOdds(cards, board, agentFlags);
            continue;
        else:
            counter = 1; # Not in sequence, nor a dup. Reset

    # If not, check inner straights. This is still wrong since we can have 2 skips in the inner flag
    counter = 1;
    lastSkip = 0; # This holds the number of steps back we had our last gap, to compensate for situations where you have X_X_XXX, which would return false when it should find odds for an inner straight
    innerFlag = False;
    for index in range(1,len(cardNums)):
        if(cardNums[index] == cardNums[index-1] + 1):
            counter += 1;
            lastSkip += 1;
            if(counter >= 4 and innerFlag):
                return innerStraightRiverOdds(cards, board, agentFlags);
        elif(index > 1 and cardNums[index] == (cardNums[index-1] + 2) and not innerFlag):
            counter += 1;
            lastSkip = 0;
            innerFlag = True;
        else:
            counter = lastSkip + 1;
            lastSkip = 0;
    
    return 0;

def innerStraightRiverOdds(cards, board, agentFlags=0):
    assert board.getDeck().getCardsPerDeck() == 52; # Fix this later @TODO
    INNER_STRAIGHT = 1;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # So here, we do the math based on a single numerical value out. Don't take one away since we don't have any
    outs = ((board.getDeck().getNumDecks() * 4) * INNER_STRAIGHT);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def outerStraightRiverOdds(cards, board, agentFlags=0):
    assert board.getDeck().getCardsPerDeck() == 52; # Fix this later @TODO
    OUTER_STRAIGHT = 2;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Here, do it based on 2 numerical value outs. Don't take one away.
    outs = ((board.getDeck().getNumDecks() * 4) * OUTER_STRAIGHT);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def flushRiverOdds(cards, board, agentFlags=0):
    # This is because I find this simpler atm. Will probably change later, if I feel like it. @TODO
    assert board.getDeck().getCardsPerDeck() == 52;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # This one has (numCardsPerDeck/Suits - 4 outs
    outs = (board.getDeck().getCardsPerDeck() / len(Suits) - 4);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def fullHouseRiverOdds(cards, board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Check if we have a three of a kind or a pair. This will be done for us by the agent flags, this is just for testing purposes @TODO
    hasThree = HandScanner().checkThreeOfAKind(cards);
    hasPair = HandScanner().checkPair(cards);
    hasTwoPair = HandScanner().checkTwoPair(cards);

    if(not hasPair): # If it has three of a kind, it'll tick this. If this is false, it has neither and cannot get a full house
        return 0;

    if(not hasTwoPair and not hasThree):
        return 0;

    outsPerCard = (board.getDeck().getNumDecks() * 4) - 1;

    if(hasThree): # Assume we already checked that we have a full house, and failed
        # The assumption above means we don't have a pair if we're running this function. So, we can check using the normal strat, but against 3 less cards
        totalOuts = outsPerCard * (cardsShown - 3);
        return (1 - ((cardsLeft - totalOuts)/cardsLeft));

    if(hasTwoPair): # If we get here, we def do not have a three of a kind. We need to least two pairs: One to be the three of a kind, one to be the pair
        numVals = [card.getCardNum() for card in cards];
        twoPairSet = set([cardNum for cardNum in numVals if numVals.count(cardNum) >= 2]);
        totalOuts = (len(twoPairSet) * outsPerCard); # The weird list compisition is to still be good to go if we have 3 pairs. The extra calcs may not be worth it though. Need to look at this in profiling. @TODO @PROFILE
        return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def fourRiverOdds(cards, board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Calc outs
    outs = (board.getDeck().getNumDecks() * len(Suits) - 3);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

'''
This function is a prototype which reverts to the inner or outer straight functions, based on what's appropriate. Has its own checking, but that may be outsourced later
'''
def straightFlushRiverOdds(cards, board, agentFlags=0):
    # Should we even waste our time?
    suits = [card.getCardSuit() for card in cards];
    suitCount = [suits.count(suit) for suit in Suits];
    if(max(suitCount) < 4):
        return 0;
    activeSuit = Suits(suitCount.index(max(suitCount)));

    # Check for an outer one first. Very similar to the handScanner's straight implementation, but checking for 4 in a row instead of five
    cardNumsFirst = [card.getCardNum() for card in cards if card.getCardSuit() == activeSuit];
    cardNumsSet = set(cardNumsFirst);
    cardNums = list(cardNumsSet);
    cardNums.sort();
    counter = 1;
    NUM_ACE_HIGH = 14;
    NUM_ACE_LOW = 1;

    # Check for outer straights
    for index in range(1,len(cardNums)):
        if(cardNums[index] == cardNums[index-1] + 1):
            counter += 1;
            if(counter >= 4):
                return outerStraightFlushRiverOdds(cards, board, agentFlags);
            continue;
        else:
            counter = 1; # Not in sequence, nor a dup. Reset

    # If not, check inner straights. This is still wrong since we can have 2 skips in the inner flag
    counter = 1;
    lastSkip = 0; # This holds the number of steps back we had our last gap, to compensate for situations where you have X_X_XXX, which would return false when it should find odds for an inner straight
    innerFlag = False;
    for index in range(1,len(cardNums)):
        if(cardNums[index] == cardNums[index-1] + 1):
            counter += 1;
            lastSkip += 1;
            if(counter >= 4 and innerFlag):
                return innerStraightFlushRiverOdds(cards, board, agentFlags);
        elif(index > 1 and cardNums[index] == (cardNums[index-1] + 2) and not innerFlag):
            counter += 1;
            lastSkip = 0;
            innerFlag = True;
        else:
            counter = lastSkip + 1;
            lastSkip = 0;
    
    return 0;

def innerStraightFlushRiverOdds(cards, board, agentFlags=0):
    assert board.getDeck().getCardsPerDeck() == 52; # Fix this later @TODO
    INNER_STRAIGHT = 1;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # So here, we do the math based on a single numerical value out. Don't take one away since we don't have any
    outs = (board.getDeck().getNumDecks() * INNER_STRAIGHT);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def outerStraightFlushRiverOdds(cards, board, agentFlags=0):
    assert board.getDeck().getCardsPerDeck() == 52; # Fix this later @TODO
    OUTER_STRAIGHT = 2;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Here, do it based on 2 numerical value outs. Don't take one away.
    outs = (board.getDeck().getNumDecks() * OUTER_STRAIGHT);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));

def fiveRiverOdds(cards, board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Calc outs
    outs = (board.getDeck().getNumDecks() * len(Suits) - 4);
    totalOuts = outs;

    return (1 - ((cardsLeft - totalOuts) / cardsLeft));
