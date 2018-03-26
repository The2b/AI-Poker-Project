'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 22 February 2018
@project Texas Hold'em AI
@file HandScanner.py

This is where I'm going to keep the functions to see what we have in our hand
'''

from enum import Enum, unique
from Card import Card, Suits
import copy

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

    '''
    Checks the parent agent's hand and the board to see if we have a pair in our hand.
    Does **NOT** calculate odds. It does, however, verify there are enough cards to form a hand before it checks anything.

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
        if(pairs): # Basically, if this list is composed based on the restrictions we have set, there's at least one pair.
            return max(pairs);

        return 0;


    '''
    Checks if the parents cards has 2 pairs

    @param Card cards[]
    @return boolean hasTwoPair
    '''
    def checkTwoPair(self, cards):
        '''
        Same as pair, but for 2 values
        '''
        cardNums = [card.getCardNum() for card in cards];
        pairCards = [nums for nums in cardNums if cardNums.count(nums) >= 2];

        if(len(pairCards) >= 4): # At least 2 pairs. If there's 3 or 4 of a kind, those'll check first and we won't bother w/ this function
            return True; # @TODO Make this return a list of three numbers: The values of pair 1, pair 2, and the kicker

        return False;


    '''
    Checks if the parents cards have a 3 of a kind. Returns 0 if there is not.

    @param Card cards[]
    @return int threeOfAKindNum
    '''
    def checkThreeOfAKind(self, cards):
        '''
        Same as pair, but the value needs to exist three times. Don't check pre-flop
        '''
        if(len(cards) >= 3): # May redo this. If so, it'll be such that the agent has a switch statement based on the stage, which executes different checks @TODO
            cardNums = [card.getCardNum() for card in cards];
            three = [nums for nums in cardNums if cardNums.count(nums) >= 3];

            if(three):
                return max(three);

        return 0;

    '''
    Checks if the parents cards have a straight @TODO all this shit

    @param Card cards[]
    @return boolean hasStraight
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
                        return True;
                    continue;
                elif(cardNums[index] == (cardNums[index-1])):
                    continue;
                counter = 1; # If it got here, the last card was neither part of the sequence nor a dup, and therefore the counter should reset

        return False;

    '''
    Checks if the parents cards have a flush. Don't check pre-flop. If there's a flush, it returns the cards' IDs. If not, returns 0

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
        
        if(count < 5):
            return 0;

        return [card.getCardID() for card in cards if card.getCardSuit() == activeSuit];

    '''
    Checks the agent's hand for a full house

    @param Card cards[]
    @return boolean hasFullHouse
    '''
    def checkFullHouse(self, cards):
        '''
        1) Check for a three of a kind. If it exists, remove those cards. If not, return false
        2) Check for a pair. If there, return true. If not, false.
        '''

        cardNums = [card.getCardNum() for card in cards];

        three = [nums for nums in cardNums if cardNums.count(nums) == 3]; # I went with == since if there are more than 3 of a card, this isn't the highest hand
        if(three):
            pair = [pairs for pairs in cardNums if (cardNums.count(pairs) >= 2 and pairs != max(three)) ]; # Can be 2 or 3, but NOT the max in three. This makes it such that if we have 2 three of a kinds, it'll still work.
            if(pair):
                return True; # I did this so that there is reliability in what we are returning. The 5 extra cycles this takes shouldn't be a huge issue, but I'll mark it for profiling to be safe. @TODO Profile this @TODO Fix this return to be more usable

        return False;

    '''
    Check the agent's hand for a four of a kind

    @param Card cards[]
    @return int fourOfAKindNum
    '''
    def checkFourOfAKind(self, cards):
        '''
        Duh
        '''
        cardNums = [card.getCardNum() for card in cards];
        four = [nums for nums in cardNums if cardNums.count(nums) >= 4];
        if(four):
            return max(four);

        return 0;

    '''
    Checks the agent's hand for a straight flush

    @param Card cards[]
    @return boolean hasStraightFlush
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
            return False;

        flushCards = [card for card in cards if card.getCardSuit() == activeSuit];
        return self.checkStraight(flushCards);

    '''
    Checks the agent's hand for a five of a kind

    @param Card cards[]
    @return int fiveOfAKindNum
    '''
    def checkFiveOfAKind(self, cards):
        cardNums = [card.getCardNum() for card in cards];
        five = [nums for nums in cardNums if cardNums.count(nums) >= 5];
        if(five):
            return five[0];
        return False;

    '''
    Returns the enum value of the best hand in a set of cards. This can then be used to run the specific function for that hand to get more detailed info on it, if needed

    @param Card cards[]
    @return int bestHand
    '''
    def checkBestHand(self, cards): # I may throw the switch statement I talked about above (checkThreeOfAKind) in here... WTF PYTHON DOESN'T HAVE A SWITCH STATEMENT?!?
        if(self.checkFiveOfAKind(cards)):
            return HandIDs.FIVE_OF_A_KIND;
        elif(self.checkStraightFlush(cards)):
            return HandIDs.STRAIGHT_FLUSH;
        elif(self.checkFourOfAKind(cards)):
            return HandIDs.FOUR_OF_A_KIND;
        elif(self.checkFullHouse(cards)):
            return HandIDs.FULL_HOUSE;
        elif(self.checkFlush(cards)):
            return HandIDs.FLUSH;
        elif(self.checkStraight(cards)):
            return HandIDs.STRAIGHT;
        elif(self.checkThreeOfAKind(cards)):
            return HandIDs.THREE_OF_A_KIND;
        elif(self.checkTwoPair(cards)):
            return HandIDs.TWO_PAIR;
        elif(self.checkPair(cards)):
            return HandIDs.PAIR;
        else:
            return HandIDs.HIGH_CARD;
