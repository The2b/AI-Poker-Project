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
'''

class OddsCalc:
    @staticmethod
    def highCard(cards):
        # Basically, this is here for completion. It'll always be true.
        return 100;

    @staticmethod
    def pair(cards, hasPair=0): # @TODO Fix this shit up
        # Remember, each card in the cards array exists. Therefore, if we have 2 cards with the same numeric value, it's 100%
        # We should optimize this a touch. Right now, this is a combination, rather than the permutation it is right now.
        # But, I'm not going to touch it right now...
        for index in cards:
            for index2 in cards:
                if(index == index2):
                    return 100;

        # At this point, it depends on how many cards we have left to go, and the odds that any of them match our current cards, or one another

    @staticmethod
    def twoPair(cards):
        '''
        We can use the pair tester to shortcut this
        1) If we don't have a pair, and there's <= 1 card left to reveal, return 0
        2) If we have a pair, run it again with the pair taken out of the array, and hasPair set to true. If it returns 0, return 0
        
        This seems overly complex math-wise. Probably going to change this later.
        '''

    @staticmethod
    def threeOfAKind(cards):
        '''
        This one's easier. Take it in a few steps.
            1) For each card we have, check if there's a three of a kind. If so, return 100
            2) For each card we have, check if there's a pair. If so, calc the odds 1 of the remaining cards to flip is the third. Then, calc if the remaining cards can get you a 3oaK off a card you don't have paired, if there's at least 2 left to flip
            3) If there's no pair, and at least 2 cards left to flip, calc odds that those 2 cards are equal to each other AND equal to a card you have
            4) If there's no pair, and only 1 card left to flip, return 0
        '''

    @staticmethod
    def straight(cards):

    @staticmethod
    def flush(cards):
        '''
        Similar to the three of a kind, we can take this in steps
        1) Do we have the flush already? If so, return 100. Only check post-flop.
        2) What are the odds we get the flush in any particular suit? We can skip suits which it is impossible to get the flush for
        '''

    @staticmethod
    def fullHouse(cards):
        '''
        We can shortcut this with the three-of-a-kind function. If that's 0, this is 0.
        While we can do the same with the pair, if that comes up true, this will.

        If we have <= 2 cards left to reveal, *and* we have neither a three of a kind OR a pair, this is 0
        '''

    @staticmethod
    def fourOfAKind(cards):
        '''
        We can shortcut this with the three-of-a-kind function. If that's 0, this is 0.
        If we don't already have a three of a kind, and there's <= 1 card left, return 0
        '''

    @staticmethod
    def straightFlush(cards):
        '''
        We can shortcut this pretty effectively, actually
        1) Can we get a flush? If not, return 0
        2) Can we get a straight? If not, return 0
        '''
