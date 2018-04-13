'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 31 March 2018
@project Texas Hold'em AI
@file AgentController.py
'''

from AgentModel import AgentModel
import OddsCalc as oc
import OddsCalcPot
from HandScanner import HandScanner
from Card import Card, CardIDs
from Deck import Deck

class AgentController:
    agent = 0;
    scanner = HandScanner();

    __CARDS_IN_HAND = 2;
    __MARGIN = .05; # The margin for staying in if the pot odds are lower than the odds of winning, and for calling if they're higher. This is a %
    __POT_ODDS_RED_FLAG_AMT = .4; # Because pot odds can never be more than 50%, this should never exceed .5. .4 means that there's a huge influx of money compared to the old pot, so we need to take special consideration

    def __init__(self, agentModel=0):
        if(agentModel != 0):
            self.agent = agentModel;
        else:
            self.agent = AgentModel();

        self.resetAgent();

    def shouldBet(self, board):
        # Calc pot odds
        # Then calc odds of winning
        # Determine which is greater
        # (At least) call or fold
        print("I'll bet");

    def shouldCheck(self, board):
        # Basically, we'll only use this is we would otherwise fold, but there's no bet to the agent
        print("I check");

    def shouldCall(self, board):
        # If the current pot odds are close to our chance of victory, use this
        print("I call");

    def shouldRaise(self, board, raiseAmt):
        # If the odds of winning are far higher than the pot odds, choose this
        # Choose the amount based on the percentage of money left & the distance between the pot odds and odds of winning? @TODO
        print("I raise");

    def shouldFold(self, board):
        # If there's too much of a bet to the agent for the risk
        print("I fold");
        self.agent.inGame = False;

    def makeDecision(self, board):
        # Indexes for victorOdds below
        WIN = 0;
        LOSE = 1;
        TIE = 2;

        # Update our flags first
        self.updateAgentFlags(board);

        # Find pot odds
        potOdds = OddsCalcPot.oddsCalcPot(board);

        # Find our odds of victory, using our odds of a hand and our opponents odds of a hand
        # Just as a reminder, this is in the form [WIN, LOSE, TIE]
        victorOdds = oc.oddsCalc(self.buildHand(board), board);

        # If we're before the turn, consider a tie a loss. This will make it such that if there's enough in the pot, we'll still go, but if there's little, we won't risk it for basically nothing
        # After the turn, stick with it if there's a high chance of a tie
        # LOL jk, that logic is already handled in OddsCalc

        # If odds of victory are low compared to pot odds, bow out or check
        if(victorOdds[WIN] + self.__MARGIN < potOdds):
            if(board.getBet() == 0):
                self.shouldCall();
            else:
                self.shouldFold(board);

        # If close, call
        elif(victorOdds[WIN] - self.__MARGIN <= potOdds and victorOdds[WIN] + self.__MARGIN >= potOdds):
            self.shouldCall(board);

        # If if high, raise
        elif(victorOdds[WIN] - self.__MARGIN > potOdds):
            self.shouldRaise(board, self.calcRaise(board)); # @TODO

        # This is most likely going to be an issue, as someone could simply all-in every time and make the agent fold
        # Looking at it again, this won't be an issue, since pot odds can never exceed 50%
        #if(potOdds > self.__POT_ODDS_RED_FLAG_AMT):

    def calcRaise(self,  board):
        pass;

    def inGame(self):
        return self.agent.inGame;

    def resetAgent(self):
        self.agent.resetAgent();
        return;

    def getHand(self):
        return self.agent.getHand();

    def drawHand(self, board):
        self.agent.setHand(board.getDeck().dealCards(self.__CARDS_IN_HAND));

    def buildHand(self, board):
        # Add our hand to the cards
        cards = [];
        for card in self.agent.getHand():
            if(card != None):
                cards.append(card);

        # And the pool
        for card in board.getPool():
            if(card != None):
                cards.append(card);

        return cards;

    # @TODO
    def updateAgentFlags(self, board):
        '''
        cards = self.buildHand(board);
        self.updateHighCardFlags(board, cards);
        self.updatePairFlags(board, cards);
        self.updateTwoPairFlags(board, cards);
        self.updateThreeOfAKindFlags(board, cards);
        self.updateStraightFlags(board, cards);
        self.updateFlushFlags(board, cards);
        self.updateFullHouse(board, cards);
        self.updateFourOfAKind(board, cards);
        self.updateStraightFlushFlags(board, cards);
        self.updateFiveOfAKind(board, cards);
        '''
        return;
    
    # @TODO Refactor either these functions or all other similar functions for consistency. Specifically, most use (self, cards, board) but these do not, due tot he optional parameter of cards.
    def updateHighCardFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        if(not self.agent.hasHighCard and not self.agent.zeroHighCard):
            if(oc.calcOddsHighCard(cards, board, self.agent) == 0):
                self.agent.zeroHighCard = True;

            elif(self.scanner.checkHighCard(cards)):
                self.agent.hasHighCard = True;

    def updatePairFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        # No shortcuts
        if(not self.agent.hasPair and not self.agent.zeroPair):
            if(oc.calcOddsPair(cards, board, self.agent) == 0):
                self.agent.zeroPair = True;

            elif(self.scanner.checkPair(cards)):
                self.agent.hasPair = True;
        return;

    def updateTwoPairFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);
        
        # Must have a pair
        if(not self.agent.hasTwoPair and not self.agent.zeroTwoPair):
            if(oc.calcOddsTwoPair(cards, board, self.agent) == 0):
                self.agent.zeroTwoPair = True;

            elif(elf.agent.hasPair):
                if(self.scanner.checkTwoPair(cards)):
                    self.agent.hasTwoPair = True;
        return;

    def updateThreeOfAKindFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        if(not self.agent.hasThree and not self.agent.zeroThree and agent.hasPair):
            if(oc.calcOddsThreeOfAKind(cards, board, self.agent) == 0):
                self.agent.zeroThree = True;

            if(self.scanner.checkThreeOfAKind(cards)):
                self.agent.hasThree = True;

        return;

    def updateStraightFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        # @TODO see if there are shortcuts
        if(not self.agent.hasStraight and not self.agent.zeroStraight):
            if(oc.calcOddsStraight(cards, board, self.agent) == 0):
                self.agent.zeroStraight = True;

            elif(self.scanner.checkStraight(cards)):
                self.agent.hasStraight = True;
        return;

    def updateFlushFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        # @TODO see if there are shortcuts
        if(not self.agent.hasFlush and not self.agent.zeroFlush):
            if(oc.calcOddsFlush(cards, board, self.agent) == 0):
                self.agent.zeroFlush = True;

            elif(self.scanner.checkFlush(cards)):
                self.agent.hasFlush = True;
        return;

    def updateFullHouseFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        if(not self.agent.hasFullHouse and not self.agent.zeroFullHouse):
            if(oc.calcOddsFullHouse(cards, board, self.agent) == 0):
                self.agent.zeroFullHouse = True;
            
            # Must have a three of a kind. Don't bother checking pair since that's a pre-req of three
            elif(self.agent.hasThree):
                if(self.scanner.checkFullHouse(cards)):
                    self.agent.hasFullHouse = True;
        return;

    def updateFourOfAKindFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        if(not self.agent.hasFour and not self.agent.zeroFour):
            if(oc.calcOddsFourOfAKind(cards, board, self.agent) == 0):
                self.agent.zeroFour = False;

            # Must have a three of a kind
            elif(self.agent.hasThree):
                if(self.scanner.checkFourOfAKind(cards)):
                    self.agent.hasFour = True;
        return;

    def updateStraightFlushFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        if(not self.agent.hasStraightFlush and not self.agent.zeroStraightFlush):
            if(oc.calcOddsStraightFlush(cards, board, self.agent) == 0):
                self.agent.zeroStraightFlush = True;

            # Must have a straight and a flush
            if(self.agent.hasStraight and self.agent.hasFlush):
                if(self.scanner.checkStraightFlush(cars)):
                    self.agent.hasStraightFlush = True;
        return;

    def updateFiveOfAKindFlags(self, board, cards=0):
        if(cards == 0):
            self.buildHand(board);

        # Must have a four of a kind
        if(not self.agent.hasFive and not self.agent.zeroFive):
            if(oc.calcOddsFiveOfAKind(cards, board, self.agent) == 0):
                self.agent.zeroFive = True;

            elif(self.agent.hasFour):
                if(self.scanner.checkFiveOfAKind(cards)):
                    self.agent.hasFive = True;

    def updateNumPairs(self, board):
        if(self.agent.hasPair):
            cardNums = [card.getCardNum() for card in self.buildHand(board)];
            numCount = [cardNums.count(i.value) for i in CardIDs];
            self.agent.numPairs = len(set(num for num in numCount if num > 1));
        else:
            self.agent.numPairs = 0;

    def updateNumThrees(self, board):
        if(self.agent.hasThree):
            cardNums = [card.getCardNum() for card in self.buildHand(board)];
            numCount = [cardNums.count(i.value) for i in CardIDs];
            self.agent.numThrees = len(set(num for num in numCount if num > 2));
        else:
            self.agent.numThrees = 0;
