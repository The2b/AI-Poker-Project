'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 31 March 2018
@project Texas Hold'em AI
@file AgentController.py
'''

import math
import pdb

import tensorflow as tf
import numpy as np

from AgentModel import AgentModel
import OddsCalc as oc
import OddsCalcPot
from HandScanner import HandScanner
from Card import Card, CardIDs
from Deck import Deck

class AgentController:
    agent = 0;
    ai = True;
    scanner = HandScanner();

    lastArgs = [];

    __CARDS_IN_HAND = 2;
    __MARGIN = .05; # The margin for staying in if the pot odds are lower than the odds of winning, and for calling if they're higher. This is a %
    __POT_ODDS_RED_FLAG_AMT = .4; # Because pot odds can never be more than 50%, this should never exceed .5. .4 means that there's a huge influx of money compared to the old pot, so we need to take special consideration
    POT_BET_CAP = 1;
    CSV_PATH = "temp.csv";
    
    def __init__(self, agentModel=0, csvPath=0, quiet=True, ai=True):
        if(agentModel != 0):
            self.agent = agentModel;
        else:
            self.agent = AgentModel(quiet=quiet);

        self.resetAgent();
        self.agent.oppoModel.setLearningRate(0.01);

        self.ai = ai;

        if(csvPath != 0):
            self.CSV_PATH = csvPath;

    def addDataToModel(self, result, agentCashAtStartOfHand=-1, oppoCashAtStartOfHand=-1, oldPotValue=-1, lastAgentAction=-1, lastOppoAction=-1, oldBetAmount=-1, newBetAmount=-1, agentHand=[-1,-1], communityPool=[-1,-1,-1,-1,-1], victorOdds=[-1,-1,-1], gameStage=-1, cardsInDeck=-1):
        fstream = open(self.CSV_PATH, 'a');

        entry = "{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{}".format(float(agentCashAtStartOfHand),float(oppoCashAtStartOfHand),float(oldPotValue),float(lastAgentAction),float(lastOppoAction),float(oldBetAmount),float(newBetAmount),float(agentHand[0]),float(agentHand[1]),float(communityPool[0]),float(communityPool[1]),float(communityPool[2]),float(communityPool[3]),float(communityPool[4]),float(victorOdds[0]),float(victorOdds[1]),float(victorOdds[2]),float(gameStage),float(cardsInDeck),int(result));

        fstream.write(entry);
        fstream.write("\n");
        fstream.close();

        ds = tf.data.TextLineDataset.from_tensors(self.agent.oppoModel.parse_csv(entry));

        self.agent.oppoModel.addDataToModel(ds);

    def submitResult(self, result):
        l = self.getLastArgs();
        if(len(l) == 0):
            return;

        self.addDataToModel(result, l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11]);
        return;

    def call(self, board):
        # If the current pot odds are close to our chance of victory, use this
        self.agent.addToCashInPot(board, board.getBet() - self.agent.getCashInPotThisRound());
        print("Agent calls");
        return 0;

    def raiseBet(self, board, raiseTo):
        # If the odds of winning are far higher than the pot odds, choose this
        # Choose the amount based on the percentage of money left & the distance between the pot odds and odds of winning? @TODO
        if(self.raiseAgentBetTo(board, raiseTo)):
            print("Agent raises the bet to",raiseTo);
            board.setBet(raiseTo);
            print("New pot:",board.getPot());
            return 1;

        else:
            print("Could not raise bet");

    def fold(self, board):
        # If there's too much of a bet to the agent for the risk
        print("I fold");
        self.agent.inGame = False;
        return 2;

    def raiseAgentBetTo(self, board, raiseTo):
        return self.agent.addToCashInPot(board, raiseTo - self.agent.getCashInPotThisRound());
    
    def storeLastArgs(self, agentCashAtStartOfHand, oppoCashAtStartOfHand, oldPotValue, lastAgentAction, lastOppoAction, oldBetAmount, newBetAmount, agentHand, communityPool, victorOdds, gameStage, cardsInDeck):
        poolCards = [-1 for i in range(5)];
        agentHandIDs = [];

        for index, card in enumerate(communityPool):
            poolCards[index] = card.getCardID().value;

        for card in agentHand:
            agentHandIDs.append(card.getCardID().value);

        self.lastArgs = [agentCashAtStartOfHand, oppoCashAtStartOfHand, oldPotValue, lastAgentAction, lastOppoAction, oldBetAmount, newBetAmount, agentHandIDs, poolCards, victorOdds, gameStage, cardsInDeck];
        return;

    def getLastArgs(self):
        return self.lastArgs;

    def makeDecision(self, board, agentStartingCash, oppoStartingCash, lastAgentAction, lastOppoAction, maxbet=-1):
        if(board.getBet() == maxbet):
            self.call(board);
        # Indexes for victorOdds below
        WIN = 0;
        LOSE = 1;
        TIE = 2;

        # Update our flags first
        #self.updateAgentFlags(board);


        # Find pot odds
        try:
            potOdds = OddsCalcPot.oddsCalcPot(board);
        except ZeroDivisionError:
            print("Current pot:",board.getPot());
            print("Current bet:",board.getBet());
            pdb.set_trace();

        # Find our odds of victory, using our odds of a hand and our opponents odds of a hand
        # Just as a reminder, this is in the form [WIN, LOSE, TIE]
        victorOdds = oc.oddsCalc(self.buildHand(board), board);

        # Store our data before we screw with anything
        self.storeLastArgs(agentStartingCash, oppoStartingCash, board.getPot(), lastAgentAction, lastOppoAction, board.getBet(), 0, self.getHand(), board.getPool(), victorOdds, board.getStage().value, len(board.getDeck().getCards()));

        # If we're before the turn, consider a tie a loss. This will make it such that if there's enough in the pot, we'll still go, but if there's little, we won't risk it for basically nothing
        # After the turn, stick with it if there's a high chance of a tie
        # LOL jk, that logic is already handled in OddsCalc

        # If odds of victory are low compared to pot odds, bow out or check
        if(victorOdds[WIN] + self.__MARGIN < potOdds):
            if(board.getBet() == 0):
                return self.call(board);
            else:
                return self.fold(board);

        # If close, call
        elif(victorOdds[WIN] - self.__MARGIN <= potOdds and victorOdds[WIN] + self.__MARGIN >= potOdds):
            return self.call(board);

        # If if high, raise
        elif(victorOdds[WIN] - self.__MARGIN > potOdds):
            return self.raiseBet(board, self.calcRaise(board, agentStartingCash, oppoStartingCash, lastAgentAction, lastOppoAction, victorOdds, maxBetAmt=maxbet) + board.getBet()); # @TODO


    '''
    Note that this uses a pot-bet cap
    '''
    def calcRaise(self, board, agentStartingCash, oppoStartingCash, lastAgentAction, lastOppoAction, victorOdds, maxBetAmt=-1, oppoModel=0):
        # A few methods of calculating how much to raise
        # 1) Scale 1:1 cash to win odds
        #return winOdds * self.agent.getCash();

        # 2) Scale 1:1 cash to win odds, with a hard cap
        #BET_CAP = 500;
        #return min(winOdds * self.agent.getCash(), BET_CAP);

        # 3) Scale the raise with our current cash, win rate, and the pot. Have a cap that scales with the pot
        #POT_MULTI_LIMIT = 4;
        #return min(board.getPot() * POT_MULTI_LIMIT, (()));

        # 4) Scale it by our ideal pot odds, with a cap based on the pot. Basically doing a binary search for the pot odds we fail
        #POT_MULTI_LIMIT = 4;
        #return min(board.getPot() * POT_MULTI_LIMIT, (());

        # First, find our max bet. The max we can raise is the amount in the pot after we call the previous bet.
        currBet = board.getBet();
        currPot = board.getPot();
        winOdds = victorOdds[0];

        poolCards = [-1 for i in range(5)];
        for index, card in enumerate(board.getPool()):
            poolCards[index] = card.getCardID().value;


        if(maxBetAmt != -1):
            maxRaise = min(maxBetAmt - board.getBet(), (currBet + currPot) * self.POT_BET_CAP);
        else:
            maxRaise = (currBet + currPot) * (self.POT_BET_CAP);
        #print("Max raise:",maxRaise);
        
        # First, see if our max bet is worth it
        maxBetPotOdds = OddsCalcPot.oddsCalcPotManual(currPot + maxRaise + currBet, currBet + maxRaise);
        
        prediction_dataset = tf.convert_to_tensor([
            [np.float64(agentStartingCash), np.float64(oppoStartingCash), np.float64(currPot), np.float64(lastAgentAction), np.float64(lastOppoAction), np.float64(currBet), np.float64(maxRaise), np.float64(self.getHand()[0].getCardID().value), np.float64(self.getHand()[1].getCardID().value), np.float64(poolCards[0]), np.float64(poolCards[1]), np.float64(poolCards[2]), np.float64(poolCards[3]), np.float64(poolCards[4]), np.float64(victorOdds[0]), np.float64(victorOdds[1]), np.float64(victorOdds[2]), np.float64(board.getStage().value), np.float64(len(board.getDeck().getCards()))]
            ]);

        #print("Prediction data:",prediction_dataset);
        #print("Type:",type(prediction_dataset));

        res = self.agent.oppoModel.model(prediction_dataset);
        #print("res type:",type(res));
        print();
        print("res:",res);
        
        realRes = tf.argmax(res, axis=1).numpy();
        #print("RealRes type:",type(realRes));
        print();
        print("RealRes:",realRes);

        #print("Predicted result of a bet of",maxRaise,":",["Call","Raise","Fold"][realRes]);

        if(winOdds > maxBetPotOdds and max(realRes) < 2):
            if(maxBetAmt != -1):
                return min(maxRaise, self.agent.getCash(), maxBetAmt - board.getBet());
            else:
                return min(self.agent.getCash(), maxRaise);

        # Use a binary search with a margin of, say, .05
        testRange = [0, maxRaise];
        MIN = 0; # Min index
        MAX = 1; # Max index
        MARGIN = .10;

        lastTest = 0;

        '''
        while(True):
            if(runs > 10):
                #pdb.set_trace(); # @DEBUG
                pass;

            testAmt = math.floor((testRange[MAX] - testRange[MIN]) / 2);

            potOdds = OddsCalcPot.oddsCalcPotManual(currBet + currPot + testAmt, currBet + testAmt);
            if((winOdds + MARGIN >= potOdds and winOdds - MARGIN <= potOdds) or testAmt == maxRaise or (testAmt - lastTest <= 1)):
                return min(maxRaise, testAmt);

            if(winOdds + MARGIN > potOdds): # Here, we know it's out of our range
                testRange[MIN] = testAmt;
                lastTest = testAmt;
                runs += 1;
                continue;

            elif(winOdds - MARGIN < potOdds):
                testRange[MAX] = testAmt;
                lastTest = testAmt;
                runs += 1;
                continue;
        '''

        # If we do have a viable opponent model, use this instead
        while(True):
            testAmt = math.floor((testRange[MAX] - testRange[MIN]) / 2);
            print("Testing value:",testAmt);

            if(testAmt == 0):
                return 0;
            
            prediction_dataset = tf.convert_to_tensor([
                [np.float64(agentStartingCash), np.float64(oppoStartingCash), np.float64(currPot), np.float64(lastAgentAction), np.float64(lastOppoAction), np.float64(currBet), np.float64(testAmt), np.float64(self.getHand()[0].getCardID().value), np.float64(self.getHand()[1].getCardID().value), np.float64(poolCards[0]), np.float64(poolCards[1]), np.float64(poolCards[2]), np.float64(poolCards[3]), np.float64(poolCards[4]), np.float64(victorOdds[0]), np.float64(victorOdds[1]), np.float64(victorOdds[2]), np.float64(board.getStage().value), np.float64(len(board.getDeck().getCards()))]
            ]);

            res = self.agent.oppoModel.model(prediction_dataset);
            realRes = tf.argmax(res, axis=1).numpy();
            print("realRes:",realRes);
            #print("Predicted result of a bet of",testAmt,":",["Call","Raise","Fold"][realRes]);


            potOdds = OddsCalcPot.oddsCalcPotManual(currBet + currPot + testAmt, currBet + testAmt);
            if((max(realRes) == 2) or (winOdds - MARGIN < potOdds)):
                testRange[MAX] = testAmt;
                lastTest = testAmt;
                continue;

            if((max(realRes) < 2) and (winOdds + MARGIN >= potOdds and winOdds - MARGIN <= potOdds) or testAmt == maxRaise or (testAmt - lastTest <= 1)):
                return min(maxRaise, testAmt);

            if(winOdds + MARGIN > potOdds): # Here, we know it's out of our range
                testRange[MIN] = testAmt;
                lastTest = testAmt;
                continue;

    def inGame(self):
        return self.agent.inGame;

    def resetRound(self):
        self.agent.resetCashInPotThisRound();
        return;

    def resetAgent(self):
        self.agent.resetAgent();
        self.lastArgs = [];
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

    def getAgentCash(self):
        return self.agent.getCash();

    def setAgentCash(self, amt):
        self.agent.setCash(amt);
        return;

    def getAgentCashInPotThisRound(self):
        return self.agent.getCashInPotThisRound();

    def isAgentSquare(self, board):
        return (self.agent.getCashInPotThisRound() == board.getBet())

    '''
    # @TODO
    def updateAgentFlags(self, board):
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
        return;
    
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
    '''
