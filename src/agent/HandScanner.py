'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 22 February 2018
@project Texas Hold'em AI
@file HandScanner.py

This is where I'm going to keep the functions to see what we have in our hand

@errorcodes
    301: best hand does not have a hand value in declareWinner()
    302: hand does not have a best hand in checkBestHand()
'''

from enum import Enum, unique
from Card import Card, Suits
import copy
import sys

#import pdb # @DEBUG

@unique
class HandIDs(Enum):
    HIGH_CARD = 0;
    PAIR = 1;
    TWO_PAIR = 2;
    THREE_OF_A_KIND = 3;
    STRAIGHT = 4;
    FLUSH = 5;
    FULL_HOUSE = 6;
    FOUR_OF_A_KIND = 7;
    STRAIGHT_FLUSH = 8;
    FIVE_OF_A_KIND = 9;

class HandScanner: # @TODO make this not a class

    def checkHighCard(self, cards):
        return (max([card.getCardNum() for card in cards]));

    '''
    Checks the parent agent's hand and the board to see if we have a pair in our hand.
    Does **NOT** calculate odds. It does, however, verify there are enough cards to form a hand before it checks anything.
    Returns -1 if there is no pair

    @param Card cards[]
    @return int pairNum
    '''
    def checkPair(self, cards):
        '''
        Here's the current process. This'll need to be profiled to see if it's effective, or if there would be a faster way.
        1) Make an empty array
        2) Populate it with the numerical values of the cards
        3) See if any value shows up more than once.
        '''

        cardNums = [card.getCardNum() for card in cards];
        pairs = [nums for nums in cardNums if cardNums.count(nums) >= 2];
        
        # Replaces Aces's 0 with 13, so that it treats the high-or-low ace properly
        while(True):
            try:
                pairs[pairs.index(0)] = 13;
            except:
                break;

        if(pairs): # Basically, if this list is composed based on the restrictions we have set, there's at least one pair.
            return max(pairs);

        return -1;


    '''
    Checks if the parents cards has 2 pairs, returns all pairs if so. If not, returns -1

    @param Card cards[]
    @return int pairs[]
    '''
    def checkTwoPair(self, cards):
        '''
        Same as pair, but for 2 values
        '''
        cardNums = [card.getCardNum() for card in cards];
        pairCards = [nums for nums in cardNums if cardNums.count(nums) >= 2];

        while(True):
            try:
                pairCards[pairCards.index(0)] = 13;
            except:
                break;

        if(len(set(pairCards)) >= 2): # At least 2 pairs. If there's 3 or 4 of a kind, those'll check first and we won't bother w/ this function
            #print("pairCards9:",pairCards); # @DEBUG
            sortedList = list(set(pairCards)); # @TODO Make this return a list of three numbers: The values of pair 1, pair 2, and the kicker
            sortedList.sort(reverse=True);
            #print(sortedList); # @DEBUG
            return sortedList;

        return -1;


    '''
    Checks if the parents cards have a 3 of a kind. Returns -1 if there is not.

    @param Card cards[]
    @return int threeOfAKindNum
    '''
    def checkThreeOfAKind(self, cards):
        '''
        Same as pair, but the value needs to exist three times. Don't check pre-flop
        '''
        if(len(cards) >= 3):
            cardNums = [card.getCardNum() for card in cards];
            three = [nums for nums in cardNums if cardNums.count(nums) >= 3];

            while(True):
                try:
                    three[three.index(0)] = 13;
                except:
                    break;

            if(three):
                return max(three);

        return -1;

    '''
    Checks if the parents cards have a straight. Returns -1 if there is none.

    @param Card cards[]
    @return int straightHigh
    '''
    def checkStraight(self, cards):
        '''
        Only bother with this if there are at least 5 cards (ie post-flop)

        This one is one of the most complex ones. I think the easiest way to do this would be the following:
        1) Create a bool shouldCount. This will be set at the end of the loop.
        2) Create an int counter, which we'll go over later.
        3) Create an int lastVal, which will keep track of the last value in the list
        4) Sort the list
        5) Step through the list.
        6) Each time through, compare the last value with the current value. If the current value is one more than the last value, increment counter.
            If not, set shouldCount to false. If it's false at the start of the loop, reset the counter.
        If the counter ever reaches 5, break the loop and return true.
        '''

        NUM_ACE_LOW = 1;
        NUM_ACE_HIGH = 14;

        if(len(cards) >= 5):
            cardNums = [card.getCardNum() for card in cards];
            cardNums.sort();
            counter = 1;

            # Add in ace highs
            for i in range(cardNums.count(NUM_ACE_LOW)):
                cardNums.append(NUM_ACE_HIGH);

            for index in range(1,len(cardNums)):
                if(cardNums[index] == (cardNums[index-1]+1)): # If this card is one higher than the last card, bump the counter and check its status
                    counter += 1;
                    if(counter >= 5):
                        oldIndex = 0;
                        while(index < (len(cardNums)-1) and index != oldIndex):
                            oldIndex = index;
                            if((cardNums[index] == (cardNums[index-1]+1) or cardNums[index] == cardNums[index-1])):
                                index += 1;
                        return cardNums[index]; # Because this list is sorted, the number we're on is the highest card
                    continue;
                elif(cardNums[index] == (cardNums[index-1])):
                    continue;
                counter = 1; # If it got here, the last card was neither part of the sequence nor a dup, and therefore the counter should reset

        return -1;

    '''
    Checks if the parents cards have a flush. Don't check pre-flop. If there's a flush, it returns the cards' IDs. If not, returns -1

    @param Card cards[]
    @return int cardNums[]
    '''
    def checkFlush(self, cards):
        '''
        1) Create a list to hold Suits values
        2) Populate the list based off the cards array.
        3) Count the number of times each value appears. If any appears 3 times, break. If >= 5, return the card IDs.
        '''

        cardSuits = [card.getCardSuit() for card in cards];
        activeSuit = -1;

        for suit in cardSuits:
            count = cardSuits.count(suit);
            if(count >= 3):
                activeSuit = suit;
                break;

        cardNums = [card.getCardNum() for card in cards if card.getCardSuit() == activeSuit];

        while(True):
            try:
                cardNums[cardNums.index(0)] = 13;
            except:
                break;
        
        cardNums.sort(reverse = True);

        if(count < 5):
            return -1;

        return [cardNums[0], cardNums[1], cardNums[2], cardNums[3], cardNums[4]];

    '''
    Checks the agent's hand for a full house. Returns -1 if there is none.

    @param Card cards[]
    @return int cards[threeOfAKind, pair] OR 0
    '''
    def checkFullHouse(self, cards):
        '''
        1) Check for a three of a kind. If it exists, remove those cards. If not, return false
        2) Check for a pair. If there, return true. If not, false.
        '''

        cardNums = [card.getCardNum() for card in cards];

        while(True):
            try:
                cardNums[cardNums.index(0)] = 13;
            except:
                break;

        three = [nums for nums in cardNums if cardNums.count(nums) == 3]; # I went with == since if there are more than 3 of a card, this isn't the highest hand
        if(three):
            pair = [pairs for pairs in cardNums if (cardNums.count(pairs) >= 2 and pairs != max(three)) ]; # Can be 2 or 3, but NOT the max in three. This makes it such that if we have 2 three of a kinds, it'll still work.
            if(pair):
                return [max(three), max(pair)];

        return -1;

    '''
    Check the agent's hand for a four of a kind. Returns -1 if there is none.

    @param Card cards[]
    @return int fourOfAKindNum
    '''
    def checkFourOfAKind(self, cards):
        '''
        Duh
        '''
        cardNums = [card.getCardNum() for card in cards];
        four = [nums for nums in cardNums if cardNums.count(nums) >= 4];

        while(True):
            try:
                four[four.index(0)] = 13;
            except:
                break;

        if(four):
            return max(four);

        return -1;

    '''
    Checks the agent's hand for a straight flush. Returns -1 if there is none.

    @param Card cards[]
    @return int straightHigh
    '''
    def checkStraightFlush(self, cards):
        '''
        1) Check for a flush, since its simpler. If not, return false. If there, create an array with the cards such that they are the suit used for the flush. for x in y where x.getSuit() == SUIT:
        2) If the resulting substring is a straight, return true.
        '''

        count = 0;
        cardSuits = [card.getCardSuit() for card in cards];
        activeSuit = 0; # This is so that if we do have a flush, we can build a list of all the cards of just that suit and check if that list has a straight
        for suit in Suits:
            count = cardSuits.count(suit);
            if(count >= 5):
                activeSuit = suit;
                break;
            
        if(count < 5):
            return -1;

        flushCards = [card for card in cards if card.getCardSuit() == activeSuit];
        return self.checkStraight(flushCards);

    '''
    Checks the agent's hand for a five of a kind. Returns -1 if there is none

    @param Card cards[]
    @return int fiveOfAKindNum
    '''
    def checkFiveOfAKind(self, cards):
        cardNums = [card.getCardNum() for card in cards];
        five = [nums for nums in cardNums if cardNums.count(nums) >= 5];

        while(True):
            try:
                five[five.index(0)] = 13;
            except:
                break;

        if(five):
            return max(five);
        return -1;

    '''
    Returns the enum value of the best hand in a set of cards. This can then be used to run the specific function for that hand to get more detailed info on it, if needed

    @param Card cards[]
    @return int bestHand
    '''
    def checkBestHand(self, cards): # I may throw the switch statement I talked about above (checkThreeOfAKind) in here... WTF PYTHON DOESN'T HAVE A SWITCH STATEMENT?!?
        if(self.checkFiveOfAKind(cards) != -1):
            return HandIDs.FIVE_OF_A_KIND;
        elif(self.checkStraightFlush(cards) != -1):
            return HandIDs.STRAIGHT_FLUSH;
        elif(self.checkFourOfAKind(cards) != -1):
            return HandIDs.FOUR_OF_A_KIND;
        elif(self.checkFullHouse(cards) != -1):
            return HandIDs.FULL_HOUSE;
        elif(self.checkFlush(cards) != -1):
            return HandIDs.FLUSH;
        elif(self.checkStraight(cards) != -1):
            return HandIDs.STRAIGHT;
        elif(self.checkThreeOfAKind(cards) != -1):
            return HandIDs.THREE_OF_A_KIND;
        elif(self.checkTwoPair(cards) != -1):
            return HandIDs.TWO_PAIR;
        elif(self.checkPair(cards) != -1):
            return HandIDs.PAIR;
        else:
            return HandIDs.HIGH_CARD;
        #elif(self.checkHighCard(cards) != -1): # Commented out for performance
        #   return HandIDs.HIGH_CARD;
        #else:
        #   print("Error! How did you get here? Exiting...");
        #   sys.exit(302);


    '''
    Takes a list of hands and decides a winner. Note that the list of hands is a list of hole cards, not a list of 7 cards

    @param Card hands[]
    @param Board board
    @return int winnerIndex. Returns a list if there's a tie.
    '''
    def declareWinner(self, hands, board):
        bestHand = []; # Holds the list of best hands

        for hand in hands:
            #print("Hand",hands.index(hand),":  ",[card.getCardID().name for card in hand]); # @DEBUG
            for card in board.getPool():
                if(card not in hand):
                    hand.append(card);

            bestHand.append(self.checkBestHand(hand));
            
            print("Agent",hands.index(hand),"best hand:", HandIDs(bestHand[hands.index(hand)]).name);


        #print("Best hand list:",bestHand); # @DEBUG

        # Check if there's more than one of a best hand
        bestID = HandIDs(max([hand.value for hand in bestHand]));

        # If there is, tie break. Its probably faster to pass all the hands than to figure out which ones are tied, build a list of only them, and check that list
        # NOTE: Because I didn't realize this had a looping dependency issue, and the lines for the called functions are very similar each time AND only a couple lines, I'm just moving them here. tb in this case refers to the old TieBreaker.py file
        '''
        if(bestHand.count(bestID) > 1):
            if(bestID == HandIDs.HIGH_CARD):
                return tb.breakHighCard(hands);
            elif(bestID == HandIDs.PAIR):
                return tb.breakPair(hands);
            elif(bestID == HandIDs.TWO_PAIR):
                return tb.breakTwoPair(hands);
            elif(bestID == HandIDs.THREE_OF_A_KIND):
                return tb.breakThreeOfAKind(hands);
            elif(bestID == HandIDs.STRAIGHT):
                return tb.breakStraight(hands);
            elif(bestID == HandIDs.FLUSH):
                return tb.breakFlush(hands);
            elif(bestID == HandIDs.FULL_HOUSE):
                return tb.breakFullHouse(hands);
            elif(bestID == HandIDs.FOUR_OF_A_KIND):
                return tb.breakFourOfAKind(hands);
            elif(bestID == HandIDs.STRAIGHT_FLUSH):
                return tb.breakStraightFlush(hands);
            elif(bestID == HandIDs.FIVE_OF_A_KIND):
                return tb.breakFiveOfAKind(hands);
            else:
                print("ERROR: Hand does not have a bestID in HandScanner.declareWinner. Exiting...");
                sys.exit(301);
            '''

        if(bestHand.count(bestID) > 1):
            if(bestID == HandIDs.HIGH_CARD):
                vals = [self.checkHighCard(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];

            elif(bestID == HandIDs.PAIR):
                vals = [self.checkPair(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];

            elif(bestID == HandIDs.TWO_PAIR):
                #pdb.set_trace(); # @DEBUG
                vals = [self.checkTwoPair(hand) for hand in hands];
                firstPair = [val[0] for val in vals];
                if(firstPair.count(max(firstPair)) > 1):
                    secondPair = [val[1] for val in vals if val[0] == max(firstPair)];
                    return [index for index in range(len(vals)) if(vals[index][0] == max(firstPair) and vals[index][1] == max(secondPair))];
                else:
                    return [index for index in range(len(vals)) if(vals[index][0] == max(firstPair))];
            
            elif(bestID == HandIDs.THREE_OF_A_KIND):
                vals = [self.checkThreeOfAKind(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];
            
            elif(bestID == HandIDs.STRAIGHT):
                vals = [self.checkStraight(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];
            
            elif(bestID == HandIDs.FLUSH): # Check all 5 nums
                vals = [self.checkFlush(hand) for hand in hands];
                firstCard = [val[0] for val in vals];
                highFirstCard = max(firstCard);

                if(firstCard.count(highFirstCard) > 1):
                    secondCard = [val[1] for val in vals if val[0] == highFirstCard];
                    highSecondCard = max(secondCard);
                    if(secondCard.count(highSecondCard) > 1):
                        thirdCard = [val[2] for val in vals if(val[0] == highFirstCard and val[1] == highSecondCard)];
                        highThirdCard = max(thirdCard);
                        if(thirdCard.count(highThirdCard) > 1):
                            fourthCard = [val[3] for val in vals if(val[0] == highFirstCard and val[1] == highSecondCard and val[2] == highThirdCard)];
                            highFourthCard = max(fourthCard);
                            if(fourthCard.count(highFourthCard) > 1):
                                fifthCard = [val[4] for val in vals if(val[0] == highFirstCard and val[1] == highSecondCard and val[2] == highThirdCard and val[3] == highFourthCard)];
                                highFifthCard = max(fifthCard);
                                return [index for index,val in enumerate(vals)  if(val == [highFirstCard, highSecondCard, highThirdCard, highFourthCard, highFifthCard])];
                            else:
                                return [index for index,val in enumerate(vals)  if(val[:-1] == [highFirstCard, highSecondCard, highThirdCard, highFourthCard])];
                        else:
                            return [index for index,val in enumerate(vals)  if(val[:-2] == [highFirstCard, highSecondCard, highThirdCard])];
                    else:
                        return [index for index,val in enumerate(vals)  if(val[:-3] == [highFirstCard, highSecondCard])];
                else:
                    return [index for index,val in enumerate(vals) if(val[0] == highFirstCard)];

            elif(bestID == HandIDs.FULL_HOUSE):
                vals = [self.checkFullHouse(hand) for hand in hands];
                threeVals = [val[0] for val in vals];
                if(threeVals.count(max(threeVals)) > 1):
                    twoVals = [val[1] for val in vals if val[0] == max(threeVals)];
                    return [index for index in range(len(vals)) if(vals[index][0] == max(threeVals) and vals[index][1] == max(twoVals))];
                else:
                    return [index for index in range(len(vals)) if(vals[index][0] == max(threeVals))];
                    
            
            elif(bestID == HandIDs.FOUR_OF_A_KIND):
                vals = [self.checkFourOfAKind(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];
            
            elif(bestID == HandIDs.STRAIGHT_FLUSH):
                vals = [self.checkStraightFlush(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];
            
            elif(bestID == HandIDs.FIVE_OF_A_KIND):
                vals = [self.checkFiveOfAKind(hand) for hand in hands];
                return [index for index in range(len(vals)) if vals[index] == max(vals)];
            
            else:
                print("ERROR: Hand does not have a bestID in HandScanner.declareWinner. Exiting...");
                sys.exit(301);


        else:
            return bestHand.index(bestID);
