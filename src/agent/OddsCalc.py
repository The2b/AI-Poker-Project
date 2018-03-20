'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 21 February 2018
@project Texas Hold'em AI
@file OddsCalc.py
'''

'''
This is going to be a set of static functions which can be called
to tally up the odds of a certain class of hand being ***a*** hand @NOTE
an agent can play. This will rely on a list of CardIDs, which will then be
decoded based on the index and length of the list.

Note that any check will go through regardless of the agent's current flags on what it has.
The agent's gameloop should only use thise func's if their respective has* flags are false

I may change this such that it calcs based on 
'''

import board as Board
import deck as Deck

'''
Calculates the odds of a hand having a playable high-card

@param Card[] cards
@param board
@param agentFlags=0

@return odds
'''
def highCard(cards, board, agentFlags=0):
    # Basically, this is here for completion. It'll always be true. Don't even bother type checking.
    return 1;

'''
Calculates the odds of a hand having a playable pair on the river
Assumes that by the turn, no pair exists

@param Board board
@param AgentModel agentFlags

@return odds
'''
def pairOnRiver(board, agentFlags=0):
    # Here, 2 + 7 - 1 cards are known. Using our outs per card val, we can calc the number of cards which will give us the pair, and go from there
    cardsShown = Stage.CARDS_ON_BOARD[board.getStage()] + board.getCardsPerHand();
    cardsLeft = (board.getCardsPerDeck() * board.getNumDecks()) - cardsShown;

    # This assumes we don't have a pair, since we wont run this if we do
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    outs = cardsShown * outsPerCard;

    # Now, we just calc the odds that we have one of our outs as the last card
    return outs/(board.getDeck().getNumDecks() * board.getDeck().getCardsPerDeck());
    

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
    cardsShown = Stage.CARDS_ON_BOARD[Stage.FLOP_BETTING_STAGE] + board.getCardsPerHand();
    cardsLeft = (board.getCardsPerDeck() * board.getNumDecks()) - cardsShown;
    
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    outs = cardsShown * outsPerCard;

    cardsToShow = board.getTotalCardsOnBoard() - Stage.CARDS_ON_BOARD[Stage.FLOP_BETTING_STAGE];

    # The number of combos to get exactly one pair
    comboSinglePair = outs * (cardsLeft - outs);
    
    # Next, we calc the odds we get the double-pair from no pair
    comboTwoPair = ((outs/cardsToShow) * ((outs-1)/(cardsToShow-1)));

    # Add the combos
    combo = comboSinglePair + comboTwoPair;
    
    # Pull the total number of combos. May macro this since I'll be calcing it a lot and it should be consistent
    totalCombos = (cardsLeft/cardsToShow) * ((cardsLeft-1)/(cardsToShow-1));

    # Return the odds of a pair combo existing
    return combo/totalCombo;

'''
Calculates the odds of a hand having a playable

@param board
@param agentFlags

@return odds
'''
def pair(board, agentFlags): # @TODO Fix this shit up
    if(agentFlags.hasPair):
        return 1;

    if(board.getStage() == Stage.FIRST_BETTING_ROUND): # If we don't have the pair, this is easy to calc
        pass;

    # At this point, it depends on how many cards we have left to go, and the odds that any of them match our current cards, or one another
    if(board.getStage() == Stage.RIVER_BETTING_ROUND):
        return 0;

    # First, we need to calculate the number of outs we have
    # We have X cards showing, and Y cards to reveal. The deck has Z cards left.
    # Since we don't have a pair, for each card showing, there are (4*Decks-1) outs
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;

    # Now that we have that number, we need to calc the odds we hit our pair from our current stage to the river
    # I'm only doing this post-flop, so this loop will handle if I get 2 pair, since that's still a pair. I may get rid of this, but I doubt it
    cardsOnBoard = Stage.CARDS_ON_BOARD[stage.value];
    cardsLeft = board.getTotalCardsOnBoard() - cardsOnBoard;

    if(board.getStage() == Stage.FLOP_BETTING_ROUND): # 2 cards left
        # Calc the odds that we get both of the next cards to be pairs. We assume we have none since we shouldn't be doing this if we do.
        oddsOfTwoPair(); # @TODO

'''
Calculates the odds of a hand having 2 playable pairs

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def twoPair(cards, board, agentFlags):
    '''
    We can use the pair tester to shortcut this
    1) If we don't have a pair, and there's <= 1 card left to reveal, return 0
    2) If we have a pair, run it again with the pair taken out of the array, and hasPair set to true. If it returns 0, return 0
        
    This seems overly complex math-wise. Probably going to change this later.
    '''
    if(agentFlags.hasTwoPair):
        return 1;

    # We'd need at least 2 cards if we don't have one pair already, and at this point, we only have one, so its a 0
    if(not agentFlags.hasPair and board.getStage() >= Stage.TURN_BETTING_ROUND):
        return 0;

    # If we don't have the pair,

    if(agentFlags.hasPair):
        pass;

'''
Calculates the odds a hand will have 2 playable pairs from the turn to the river
'''
def twoPairTurnToRiver(board, agentFlags):
    pass;

'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def threeOfAKind(cards, board, agentFlags):
    '''
    This one's easier. Take it in a few steps.
        1) For each card we have, check if there's a three of a kind. If so, return 1
        2) For each card we have, check if there's a pair. If so, calc the odds 1 of the remaining cards to flip is the third. Then, calc if the remaining cards can get you a 3oaK off a card you don't have paired, if there's at least 2 left to flip
        3) If there's no pair, and at least 2 cards left to flip, calc odds that those 2 cards are equal to each other AND equal to a card you have
        4) If there's no pair, and only 1 card left to flip, return 0
    '''
    if(agentFlags.hasThreeOfAKind):
        return 1;

    if(agentFlags.hasPair):



'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def straight(cards, board, agentFlags):
    pass;

'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def flush(cards, board, agentFlags):
    '''
    Similar to the three of a kind, we can take this in steps
    1) Do we have the flush already? If so, return 1. Only check post-flop.
    2) What are the odds we get the flush in any particular suit? We can skip suits which it is impossible to get the flush for
    '''

'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def fullHouse(cards, board, agentFlags):
    '''
    We can shortcut this with the three-of-a-kind function. If that's 0, this is 0.
    While we can do the same with the pair, if that comes up true, this will.

    If we have <= 2 cards left to reveal, *and* we have neither a three of a kind OR a pair, this is 0
    '''

'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def fourOfAKind(cards, board, agentFlags):
    '''
    We can shortcut this with the three-of-a-kind function. If that's 0, this is 0.
    If we don't already have a three of a kind, and there's <= 1 card left, return 0
    '''

'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''
def straightFlush(cards, board, agentFlags):
    '''
    We can shortcut this pretty effectively, actually
    1) Can we get a flush? If not, return 0
    2) Can we get a straight? If not, return 0
    '''

'''
Calculates the odds of a hand having a playable

@param Card[] cards
@param board
@param agentFlags

@return odds
'''

def fiveOfAKind(cards, board, agentFlags):
    '''
    If we only have one deck, return 0
    If we previously determined we can't get a four of a kind, return 0
    Else, do maths
    '''

    if(board.getDeck().getNumDecks() <= 1):
        return 0;

    if(agentFlags.hasFive):
        return 1;

    if(board.getStage() == Stage.FINAL_BETTING_ROUND):
        return 0;

    
