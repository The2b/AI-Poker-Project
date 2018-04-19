'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 03 April 2018
@project Texas Hold'em AI
@file GameRunner.py
@errorcodes
    401: Left the game loop too early
    402: First argument, the number of agents, could not be coerced into an int
'''

'''
Manages agents, runs the game
'''

import sys # argv, exit
#import pdb # @DEBUG
#import cProfile # @DEBUG
#import timeit # @DEBUG

from Board import Board, Stage
from AgentController import AgentController
from HandScanner import HandScanner

NUM_AGENTS = 2;
MAX_BETS = 4;
ANTE = 100;
STARTING_CASH = 20000;

def printHelp():
    pass;

def pcTurn(agent, board, maxBet):
    print();
    print("Your hand:",[card.getCardID().name for card in agent.getHand()]);
    print("Community pool:",[card.getCardID().name for card in board.getPool()]);
    print("Bet to you:",board.getBet() - agent.getAgentCashInPotThisRound());
    print("Total bet:",board.getBet());
    print("Your bank:",agent.getAgentCash());
    print("Current pot:",board.getPot());
    print("Current stage:",board.getStage().name);
    print();
    cmd = input("Command (c[all],f[old],q[uit],BetAmount(#)): ");
    try:
        if(cmd[0] == 'c'):
            agent.call(board);
            return 0;
        elif(cmd[0] == 'f'):
            agent.fold(board);
            return 2;
        elif(cmd[0] == 'q'):
            sys.exit(0);
        elif(cmd.isdigit()):
            if(int(cmd) > maxBet):
                print("Not all players acn afford that amount");
                print("Maximum bet:",maxBet);
                return -1;
            elif(int(cmd) < board.getBet() - agent.getAgentCashInPotThisRound()):
                print("Must at least exceed the bet to you by 1 chip if you want to raise.");
                return -1;
            else:
                agent.raiseBet(board, int(cmd));
                return 1;
        else:
            return -1;
    except IndexError:
        return -1;

def makeGame(csvPath):
    '''
    try:
        assert type(sys.argv[1]) == int;
    except:
        printHelp();
        sys.exit(402);
    '''

    # Build agents
    '''
    numAgents = sys.argv[1];
    agents = [AgentController() for i in range(numAgents)];
    '''
    agents = [];
    for i in range(NUM_AGENTS):
        agents.append(AgentController(csvPath=csvPath));

    [agent.setAgentCash(STARTING_CASH) for agent in agents];

    running = True;

    bets = 0;
    while(min([agent.getAgentCash() for agent in agents]) > ANTE):
        print();
        print();
        print("="*128);
        print();
        print();
        # Create the board
        board = Board();
        board.setBet(ANTE);

        [agent.resetAgent() for agent in agents];
        [agent.agent.addToCashInPot(board, ANTE) for agent in agents];
        [agent.resetRound() for agent in agents];

        # Draw a hand for each agent
        [agent.drawHand(board) for agent in agents];

        # Start with a minimum bet, ante-like
        lastAgentActions = [-1 for agent in agents];
        agentStartingCash = [agent.getAgentCash() for agent in agents];
        agents[1].ai = False; # Allow human control

        # And the game loop. This is done as long as there is more than one agent in the game, and we are not finished with the final betting round
        while([agent.inGame() for agent in agents].count(True) > 1 and board.getStage() != Stage.SHOWDOWN):
            while([agent.isAgentSquare(board) for agent in agents if agent.inGame()].count(False) > 0 and len([agent for agent in agents if agent.inGame()]) > 1):
                for index, agent in enumerate(agents):
                    #if(bets >= MAX_BETS):
                    #    break;
                    if(agent.inGame() and not agent.isAgentSquare(board)):
                        maxBet = min([agent.getAgentCash() + agent.getAgentCashInPotThisRound() for agent in agents if agent.inGame()]);

                        if(agent.ai):
                            print("\nAgent",index,"choosing...\n");

                            lastAgentActions[index] = agent.makeDecision(board,agentStartingCash[index],agentStartingCash[(index+1) % 2],lastAgentActions[index],lastAgentActions[(index+1) % 2],maxbet=maxBet);
                            
                            agents[(index + 1) % 2].submitResult(lastAgentActions[index]);

                            if((not agent.inGame()) and ([agent.inGame() for agent in agents].count(True) == 1)):
                                print("\nAgent",[agents.index(agent) for agent in agents if agent.inGame()][0],"wins by default\n");
                                [agent.agent.addCash(board.getPot()) for agent in agents if agent.inGame()];
                                break; 

                        else:
                            waiting = -1; # While we're waiting on the player to give a valid input
                            while(waiting == -1):
                                waiting = pcTurn(agent, board, maxBet);
                            
                            lastAgentActions[index] = waiting;
                            agents[(index + 1) % 2].submitResult(lastAgentActions[index]);

                            if(waiting == 2):
                                break;
                '''
                bets += 1;
                
                if(len([agent for agent in agents if agent.inGame()]) > 1 and [agent.isAgentSquare(board) for agent in agents if agent.inGame()].count(False) >= 0):
                    for agent in [agent for agent in agents if agent.inGame() and not agent.isAgentSquare(board)]:
                        if(agent.ai):
                            agentIndex = agents.index(agent);
                            lastAgentActions[agentIndex] = agent.makeDecision(board,agentStartingCash[agentIndex],agentStartingCash[(agentIndex +1) % 2],lastAgentActions[agentIndex],lastAgentActions[(agentIndex+1) % 2],maxbet=maxBet);

                            agents[(agentIndex +1) % 2].submitResult(lastAgentActions[agentIndex]);
                        else:
                            waiting = -1;
                            while(waiting == -1):
                                waiting = pcTurn(agent, board);
                            
                            lastAgentActions[index] = waiting;
                '''
            # Change the stage
            board.setStage(board.getStage().nextStage());
            [agent.resetRound() for agent in agents];
            board.setBet(1);
            print("\nStage:",board.getStage(),"\n");

        # One winner or in showdown
        if(board.getStage() == Stage.SHOWDOWN):
            for index, agent in enumerate(agents):
                print("Agent",index,"hand:",[card.getCardID().name for card in agent.getHand()]);
            print("Community pool:",[card.getCardID().name for card in board.getPool()]);
            print();

            hands = [agent.getHand() for agent in agents if agent.inGame()];
            winnerIndex = HandScanner().declareWinner(hands, board);
            
            if(type(winnerIndex) == int):
                winner = winnerIndex;
                print("Pot:", board.getPot());
                [agent for agent in agents if agent.inGame()][winner].agent.addCash(board.getPot());

            elif(type(winnerIndex) == list):
                if(len(winnerIndex) == 1):
                    print("Pot:", board.getPot());
                    winner = winnerIndex[0];
                    [agent for agent in agents if agent.inGame()][winner].agent.addCash(board.getPot());
                else:
                    print("Pot:", board.getPot());
                    winner = winnerIndex;
                    for i in range(len(winnerIndex)):
                        [agent.agent.addCash(board.getPot()/2) for agent in agents if agent.getHand() == hands[winnerIndex[i]]];
            print("Winner: agent",winner);

        elif([agent.inGame() for agent in agents].count(True) == 1): # If we only have one agent which is still in the game...
            winnerIndex = agents.index([agent for agent in agents if agent.inGame()][0]);
            print("Winner: agent",winnerIndex);

        else:
            print("You shouldn't be here, as the game loop exited too early. Exiting...");
            sys.exit(401);

    print("Game Over!");


if __name__ == '__main__':
    makeGame("/home/the2b/Documents/school/ai/project/src/test6.csv");
    #cProfile.run('makeGame()');
    #timer = timeit.timeit(stmt="makeGame()", setup="from __main__ import makeGame", number=100);
    #print("Time over 100 iterations:",timer);
    #print("Average time per iteration:",timer/100);
    
