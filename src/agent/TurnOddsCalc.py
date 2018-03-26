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

from Board import Board, Stage
from Deck import Deck
from Card import Suits
from HandScanner import HandScanner


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
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();
    
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    totalOuts = cardsShown * outsPerCard;

    # Only hit one
    oddsOne = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1))); # odds you hit the turn + odds you miss the turn and hit the river

    # Hit two
    oddsTwo = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    # Total
    return (oddsOne + oddsTwo);

def twoPairTurnToRiverFromZero(board, agentFlags=0):
    # Same as above
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand(); # I should store this in agent flags @TODO
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # We have the same number of outs, but we only calc the combos which give us 2 pair
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    totalOuts = cardsShown * outsPerCard;
    
    oddsTwo = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    return oddsTwo;

def twoPairTurnToRiverFromOne(board, agentFlags=0):
    # Same as above
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand(); # I should store this in agent flags @TODO
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Outs are the same, safe for the one pair we already have. For simplicity's sake, I'm going to count 4 of a kind as 2 pair. This is still a hair off tho, since we'll only have 2 outs for one deck for our pair'd card. However, this should be irrelevant. Still, going to mark it @TODO
    outsPerCard = ((board.getDeck().getNumDecks())*4)-1;
    totalOuts = (cardsShown - 2) * outsPerCard;

    # Odds we get two pair
    oddsTwo = (totalOuts / cardsLeft) * ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1)));

    # Odds we get three pair. Still gunna count it for accuracy
    oddsThree = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    return (oddsTwo + oddsThree);

'''
Calculates the odds of a hand having a playable three of a kind from the turn
Use when the hand has no pairs already
@TODO Do something about the "from one" and "from two" to make it more clear that "from one" means unpaired cards and "from two" means paired cards

@param board
@param agentFlags=0

@return odds
'''
def threeTurnToRiverFromOne(board, numUnmatched, agentFlags=0): # May move numUnmatched (or more specifically, numMatched) to agentFlags @TODO
    # Same as above
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Our outs are based on the number of unmatched cards (numbers) we have. We also can't use the pair out formula, since the second out will only have 2 matches + 4 per deck after the first
    firstOutPerCard = (4 * board.getDeck().getNumDecks()) - 1;
    firstOuts = firstOutPerCard * numUnmatched;
    secondOuts = (4 * board.getDeck().getNumDecks()) - 2; # This number is flat; It will only apply to one specific card, not every card like the pair formula aboved

    oddsPair = (firstOuts / cardsLeft);
    oddsThree = (secondOuts / (cardsLeft - 1));
    
    return (oddsPair * oddsThree);

'''

'''
def threeTurnToRiverFromTwo(board, numMatched, agentFlags=0): # May move numUnmatched (or more specifically, numMatched) to agentFlags @TODO
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Total outs are described by the outs per card * numMatched
    # Since that means we have a pair, we only have 2 of each number left
    outsPerCard = (4 * (board.getDeck().getNumDecks())) - 2;
    totalOuts = outsPerCard * numMatched;

    # Outs are for three or four of a kind
    # First three
    oddsThree = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * ((totalOuts) / (cardsLeft - 1)));

    # Now four
    oddsFour = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    return (oddsThree + oddsFour);

'''
This is a prototype for summing up the odds of a three of a kind of a given hand. This may be removed, since it is so far different from the rest of the library
'''
def threeTurnToRiver(board, numUnmatched, numMatched, agentFlags=0):
    # First, get the total odds of matched cards
    twoOdds = threeTurnToRiverFromTwo(board, numMatched, agentFlags);

    # Then unmatched
    oneOdds = threeTurnToRiverFromOne(board, numUnmatched, agentFlags);

    return (twoOdds + oneOdds);


'''
This one may be easier than I'm thinking. We will need to know if we have two outer outs (where we can have left & left, left & right, or right & right), two inner outs, or one inner and one outer out
'''
def straightTurnToRiver(cards, board, agentFlags=0):
    # This is a bitch. Valid options:
    #   2 out
    #   1 in 1 out
    #   2 in
    # So I need to put in checks for this, making it a pain in the dick
    # One way I could go about it would be to check if we have three numbers in a row. If we do, we have 2 out sets on either side
    # If we have two in a row, followed by an interruption of exactly one, and then the last card. If we do, we have the inner, along w/ two outers as our out set
    # If we have exactly two interruptions, we have an inside

    MAX_SKIPS = 2; # Hand size - (cardsPerHand - cardsLeft)
    MIN_NEEDED = 3; # The amount of cards we need in the sequence
    MAX_NEEDED = 4;
    MAX_STEPS = MAX_SKIPS + MIN_NEEDED;

    NUM_ACE_LOW = 1;
    NUM_ACE_HIGH = 14;

    # So I'm going to write this to check it on a card-by-card basis. I want to avoid this because its O(n^2), but I'm not sure there's a better way atm.
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();
        
    # Clear out dups
    cardNums = list(set([card.getCardNum() for card in cards]));
    cardNums.sort();

    # Vars for our iteration
    currSkips = 0;
    counter = 1;
    maxCounter = 1;
    aceFlag = False;

    # So here, we keep a counter of skips and hits. If hits get to 3, go to the function required based on the skip counter
    if(cardNums[0] == NUM_ACE_LOW):
        aceFlag = True;

    for index in range(1,len(cardNums)):
        if(cardNums[index] == NUM_ACE_HIGH):
            aceFlag = True;

        if(cardNums[index] == cardNums[index-1] + 1):
            counter += 1;
        elif(cardNums[index] == cardNums[index-1] + 2):
            counter += 1;
            currSkips += 1;
        elif(cardNums[index] == cardNums[index-1] + 3):
            counter += 1;
            currSkips += 2;
        else:
            # I'm kinda upset there's no label operation here. Why does python lack so many good features?
            if(counter > maxCounter):
                maxCounter = counter;

            counter = 1;
            currSkips = 0;
            if(cardNums[index] == NUM_ACE_LOW or cardNums[index] == NUM_ACE_HIGH):
                aceFlag = True;
            else:
                aceFlag = False;

            continue;

        if(currSkips > MAX_SKIPS):
            if(counter >= MIN_NEEDED):
                break;
            counter = 1;
            currSkips = 0;
            if(cardNums[index] == NUM_ACE_LOW or cardNums[index] == NUM_ACE_HIGH):
                aceFlag = True;
            else:
                aceFlag = False;

            continue;

    # While we can have 3, 4, or 5 here, I'm ignoring 5 since we should have already checked that before we wind up in here
    if(maxCounter >= MAX_NEEDED):
        # Handle size 4 straights w/ 2 cards to go
        # If we start or end at an ace, we only have one side to get the outs
        #totalOuts = (board.getDeck().getNumDecks() * 4);
        if(currSkips < 2):
            return(straightTurnToRiverFromFour(cards, board, currSkips, 2, aceFlag));
        elif(currSkips == 2):
            return(straightTurnToRiverFromFour(cards, board, currSkips, 0, aceFlag));
        else:
            return -1;

    elif(maxCounter == MIN_NEEDED):
        # Handle size 4 straights w/ 2 cards to go
        # If we start or end at an ace, we only have one side to get the outs
        #totalOuts = (board.getDeck().getNumDecks() * 4);
        if(currSkips < 2):
            return(straightTurnToRiverFromThree(cards, board, currSkips, 2, aceFlag));
        elif(currSkips == 2):
            return(straightTurnToRiverFromThree(cards, board, currSkips, 0, aceFlag));
        else:
            return -1;
    
    else:
        return 0;


'''
Note outsideOuts references the number of sides, NOT the number of outs we may have total.

Because of this, 0 insideOuts and 2 outsideOuts w/o aceFlag will give higher odds than 1 insideOut and 2 outsideOuts, since we only have one card we can get on either side, and one in the mid, totaling 3.
'''
def straightTurnToRiverFromThree(cards, board, insideOuts, outsideOuts, aceFlag):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    outsPerCard = 4 * board.getDeck().getNumDecks();

    # First, handle 0-2
    if(outsideOuts == 2):
        if(insideOuts == 0):
            if(not aceFlag):
                # We have 2*4*decks on the first draw, and 2*4*decks on the second draw
                totalOuts = 2 * outsPerCard;
                
                return ((totalOuts / cardsLeft) * (totalOuts / (cardsLeft - 1)));

            else:
                totalOuts = outsPerCard;

                # We have 2*4*decks on the first draw, and 2*4*decks on the second draw
                return ((totalOuts / cardsLeft) * (totalOuts / (cardsLeft - 1)));

        elif(insideOuts == 1):
            if(not aceFlag):
                # We require the inside out, and an outside out
                # Isn't it the same as the one w/o ace from above
                pass;
                
    # Next, handle 1-2
    # Finally, handle 2-0
    # @TODO
    return;

'''
Note outsideOuts references the number of sides, NOT the number of outs we may have total
'''
def straightTurnToRiverFromFour(cards, board, insideOuts, outsideOuts, aceFlag): # @TODO Create
    # First, handle outside
    # Then, handle inside
    pass;


'''

'''
def flushTurnToRiver(cards, board, agentFlags=0):
    cardSuits = [card.getCardSuit() for card in cards];
    numSuits = [cardSuits.count(suit) for suit in Suits];
    maxSuit = max(numSuits);

    if(maxSuit < 3):
        return 0;
    elif(maxSuit == 3):
        return flushTurnToRiverFromThree(board);
    elif(maxSuit == 4):
        return flushTurnToRiverFromFour(board);
    elif(maxSuit >= 5):
        return 1;

'''

'''
def flushTurnToRiverFromThree(board, agentFlags=0):
    # @TODO make this more general at some point. I just don't feel like handling this here, and am very, VERY deeply regretting making deck-size an option
    assert board.getDeck().getCardsPerDeck() == 52;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Our outs are values - 3. This also means our cards are 
    # @TODO generalize this at some point. I just don't give a damn atm.
    totalOuts = ((board.getDeck().getCardsPerDeck() / len(Suits)) * board.getDeck().getNumDecks()) - 3 # The three is hard-coded cuz that's kinda the point of the method...

    # Both need to be the active suit
    return ((totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1)));

'''

'''
def flushTurnToRiverFromFour(board, agentFlags=0):
    # @TODO make this more general at some point. I just don't feel like handling this here, and am very, VERY deeply regretting making deck-size an option
    assert board.getDeck().getCardsPerDeck() == 52;

    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Outs are the number of cards in X suit minus the four we already have
    totalOuts = ((board.getDeck().getCardsPerDeck() / len(Suits)) * board.getDeck().getNumDecks()) - 4;

    # One active suit
    oddsFive = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1)));

    oddsSix = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    return (oddsFive + oddsSix);


'''

'''
def fullHouseTurnToRiver(cards, board, agentFlags=0):
    scanner = HandScanner();
    
    # First, let's do three of a kind
    if(scanner.checkThreeOfAKind(cards)):
        return fullHouseTurnToRiverFromThree(board, agentFlags);
    
    # Next, two pair. This has to go before pair because this will trip both
    elif(scanner.checkTwoPair(cards)):
        return fullHouseTurnToRiverFromTwoPair(board, agentFlags);
    
    # And pair
    elif(scanner.checkPair(cards)):
        return fullHouseTurnToRiverFromPair(board, agentFlags);

    else:
        return 0;
    
'''

'''
def fullHouseTurnToRiverFromPair(board,agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # One pair is made, and either of the now two pairs are hit a second time

    # First, we'll take the odds of hitting a second pair
    pairOutsPerCard = (board.getDeck().getNumDecks() * 4) - 1;
    pairableCards = cardsShown - 2;
    totalOuts = pairOutsPerCard * pairableCards;

    pairOdds = (totalOuts / cardsLeft)# + (1 - (totalOuts / (cardsLeft - 1)));

    # Next, the odds of hitting the three. Assume two pairs can be hit, since if we had 2 before, we're not calling this one
    NUM_PAIRS = 2;

    threeOutsPerCard = (board.getDeck().getNumDecks() * 4) - 2;
    totalOuts = threeOutsPerCard * NUM_PAIRS;

    threeOdds = (totalOuts / cardsLeft)# + (1 - (totalOuts / (cardsLeft - 1)));

    # We need both
    return pairOdds * threeOdds;

'''

'''
def fullHouseTurnToRiverFromThree(board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    # Here, we just need one pair from anything but the three cards we already have
    outsPerCard = (board.getDeck().getNumDecks() * 4) - 1;
    totalOuts = (outsPerCard * (cardsShown - 3));

    # Hit the pair
    oddsPair = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1)));

    # Hit a second 3 of a kind
    oddsThree = ((totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1)));

    return oddsThree + oddsPair;


def fullHouseTurnToRiverFromTwoPair(board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    NUM_PAIRS = 2;

    # This one is a pain in the dick. Valid sets are...
    #   1) One pair, three of a kind, one irrelevant
    #   2) One pair, four of a kind
    #   3) Two three of a kinds

    # I'll write them all individually, then merge them where possible
    
    # Instances 1 & 3
    outsPerCard = (board.getDeck().getNumDecks() * 4) - 1;
    totalOuts = (outsPerCard * NUM_PAIRS);

    oddsOneThree = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1)));
    oddsTwoThrees = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    # Instance 2
    # Require two of the same card.
    # Uses outsPerCard first because I need to subtract an additional out since the original definition is for un-paired, while I'm using it here for paired
    # The second usage is because I am targeting one specific card number, rather than the 2 totalOuts is multiplied by
    oddsFour = (((outsPerCard - 1) * 2) / cardsLeft) * ((outsPerCard - 1) / (cardsLeft - 1));

    return (oddsOneThree + oddsTwoThrees + oddsFour);


'''

'''
def fourTurnToRiver(cards, board, agentFlags=0):
    cardNums = [card.getCardNum() for card in cards];
    maxCards = max([cardNums.count(card.getCardNum()) for card in cards]);

    if(maxCards < 2):
        return 0;

    elif(maxCards == 2):
        return fourTurnToRiverFromTwo(board, agentFlags);

    elif(maxCards == 3):
        return fourTurnToRiverFromThree(board, agentFlags);

    elif(maxCards == 4): # Should do checks before this func, but I'll be redundant here anyway
        return 1;

    else:
        return -1; # Error

'''

'''
def fourTurnToRiverFromTwo(board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    totalOuts = (board.getDeck().getNumDecks() * 4) - 2;

    # Need both to be outs
    return ((totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1)));

'''
f
'''
def fourTurnToRiverFromThree(board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    totalOuts = (board.getDeck().getNumDecks() * 4) - 3;

    oddsFour = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1)));

    oddsFive = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    return (oddsFour + oddsFive);

'''

'''
def straightFlushStuff(board, agentFlags=0): # @TODO Create function
    pass;


'''

'''
def fiveTurnToRiver(cards, board, agentFlags=0):
    cardNums = [card.getCardNum() for card in cards];
    maxCards = max([cardNums.count(card.getCardNum()) for card in cards]);

    if(maxCards < 3):
        return 0;

    elif(maxCards == 3):
        return fiveTurnToRiverFromThree(board, agentFlags);

    elif(maxCards == 4):
        return fiveTurnToRiverFromFour(board, agentFlags);

    elif(maxCards >= 5):
        return 1;

    else:
        return -1;

'''

'''
def fiveTurnToRiverFromThree(board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    totalOuts = (board.getDeck().getNumDecks() * 4) - 3;

    return ((totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1)));

'''

'''
def fiveTurnToRiverFromFour(board, agentFlags=0):
    cardsShown = board.getCardsOnBoard() + board.getCardsPerHand();
    cardsLeft = board.getDeck().getCardsLeft();
    cardsToShow = board.getTotalCardsOnBoard() - board.getCardsOnBoard();

    totalOuts = (board.getDeck().getNumDecks() * 4) - 3;

    oddsFive = (totalOuts / cardsLeft) + ((1 - (totalOuts / cardsLeft)) * (totalOuts / (cardsLeft - 1)));

    oddsSix = (totalOuts / cardsLeft) * ((totalOuts - 1) / (cardsLeft - 1));

    return (oddsFive + oddsSix);

