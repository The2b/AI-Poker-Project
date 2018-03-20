'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 15 March 2018
@project Texas Hold'em AI
@file TurnOddsCalc.py
'''

'''
Having one odds calc file was getting too crowded for my liking, so I'm dividing them up into their stages. The main one will be a combo of them.

I need to add some consistency to this shit
'''

from board import Board, Stage
from deck import Deck
from card import Suit


'''
Calculates the odds of a hand having a playable pair on the turn or river
Assumes that by the flop, no pair exists
Also adds the odds of a 2 pair

@param Board board
@param AgentModel agentFlags

@return odds
'''

def pairTurnToRiver(board, agentFlags=0):
    # First, calc the odds we only get one pair
    # This means we're calcing the odds we get one out, and one non-out
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();
    
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    outs = cardsShown * outsPerCard;


    # The number of combos to get exactly one pair
    comboSinglePair = outs * (cardsLeft - outs);
    
    # Next, we calc the odds we get the double-pair from no pair
    comboTwoPair = twoPairTurnToRiverFromZero(board,agentFlags);

    # Add the combos
    pairCombo = comboSinglePair + comboTwoPair;
    
    # Pull the total number of combos. May macro this since I'll be calcing it a lot and it should be consistent
    totalCombo = (cardsLeft/cardsToShow) * ((cardsLeft-1)/(cardsToShow-1));

    # Return the odds of a pair combo existing
    return pairCombo/totalCombo;


def twoPairTurnToRiverFromZero(board, agentFlags=0):
    # Same as above
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand(); # I should store this in agent flags @TODO
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # We have the same number of outs, but we only calc the combos which give us 2 pair
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    outs = cardsShown * outsPerCard;
    
    comboTwoPair = ((outs/cardsToShow) * ((outs-1)/(cardsToShow-1)));
    totalCombo = (cardsLeft/cardsToShow) * ((cardsLeft-1)/(cardsToShow-1));

    return comboTwoPair/totalCombo;

def twoPairTurnToRiverFromOne(board, agentFlags=0):
    # Same as above
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand(); # I should store this in agent flags @TODO
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Outs are the same, safe for the one pair we already have. For simplicity's sake, I'm going to count 4 of a kind as 2 pair. This is still a hair off tho, since we'll only have 2 outs for one deck for our pair'd card. However, this should be irrelevant. Still, going to mark it @TODO
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    outs = (cardsShown-2) * outsPerCard;

    # Now we need at least one more pair from that, but we can also have 2 more pairs from it.
    # First, combos which lead to 3 pairs
    comboThreePair = ((outs/cardsToShow)*((outs-1)/(cardsToShow-1)));

    # Next, exactly two pair
    comboTwoPair = outs * (cardsLeft - outs);

    totalCombo = (cardsLeft/cardsToShow) * ((cardsLeft-1)/(cardsToShow-1));

    return (comboThreePair + comboTwoPair)/totalCombo;

'''
Calculates the odds of a hand having a playable three of a kind from the turn
Use when the hand has no pairs already

@param board
@param agentFlags=0

@return odds
'''
def threeTurnToRiverFromOne(board, agentFlags=0, numUnmatched):
    # Same as above
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Our outs are based on the number of unmatched cards (numbers) we have. We also can't use the pair out formula, since the second out will only have 2 matches + 4 per deck after the first
    firstOutPerCard = (4*board.getDeck().getNumDecks()) - 1;
    firstOuts = firstOutPerCard * numUnmatched;
    secondOuts = (4*board.getDeck().getNumDecks()) - 2; # This number is flat; It will only apply to one specific card, not every card like the pair formula aboved

    totalCombo = (cardsLeft/cardsToShow) * ((cardsLeft-1)/(cardsToShow-1));

    return (firstOuts + secondOuts)/totalCombo;


'''

'''
def threeTurnToRiverFromTwo(board, agentFlags=0, numMatched):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Outs are for three or four of a kind
    # First four. Note that this has the same requirement of the second card being flat instead of linear
    firstOutsPerCard = (4 * board.getDeck().getNumDecks()) - 1;
    secondOut = (4 * board.getDeck().getNumDecks()) - 2;

    firstOutCombo = firstOutsPerCard * numMatched;
    secondOutCombo = secondOut;

    fourCombo = (firstOutCombo * secondOutCombo) / (cardsToShow * (cardsToShow - 1));

    # Now three
    threeCombo = firstOutsPerCard * (cardsLeft - firstOutsPerCard);

    totalCombo = (cardsLeft/cardsToShow) * ((cardsLeft-1)/(cardsToShow-1));

    return (firstOuts + secondOuts)/totalCombo;

'''
This is a prototype for summing up the odds of a three of a kind of a given hand. This may be removed, since it is so far different from the rest of the library
'''
def threeTurnToRiver(board, agentFlags=0, numUnmatched, numMatched):
    pass;


'''
This one may be easier than I'm thinking. We will need to know if we have two outer outs (where we can have left & left, left & right, or right & right), two inner outs, or one inner and one outer out
'''
def straightTurnToRiverFromThree(cards, board, agentFlags=0):
    pass;


'''

'''
def straightTurnToRiverFromFour(cards, board, agentFlags=0):
    pass;


'''

'''
def flushTurnToRiverFromThree(board, agentFlags=0):
    # @TODO make this more general at some point. I just don't feel like handling this here, and am very, VERY deeply regretting making deck-size an option
    assert board.getDeck().getCardsPerDeck() == 52;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = (board.getDeck().getCardsPerDeck() * board.getDeck().getNumDecks()) - cardsShown;
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Our outs are values - 3. This also means our cards are 
    # @TODO generalize this at some point. I just don't give a damn atm.
    outs = (board.getDeck().getCardsPerDeck() / len(Suit) * board.getDeck().getNumDecks()) - 3 # The three is hard-coded cuz that's kinda the point of the method...

    # Both need to be hearts

'''

'''
def flushTurnToRiverFromFour(board, agentFlags=0):
    pass;


'''

'''
def fullHouseTurnToRiverFromTwo(board,agentFlags=0):
    pass;


'''

'''
def fullHouseTurnToRiverFromThree(board, agentFlags=0):
    pass;


'''

'''
def fourTurnToRiverFromTwo(board, agentFlags=0):
    pass;


'''

'''
def fourTurnToRiverFromThree(board, agentFlags=0):
    pass;


'''

'''
def straightFlushStuff(board, agentFlags=0):
    pass;


'''

'''
def fiveTurnToRiverFromThree(board, agentFlags=0):
    pass;


'''

'''
def fiveTurnToRiverFromFour(board, agentFlags=0):
