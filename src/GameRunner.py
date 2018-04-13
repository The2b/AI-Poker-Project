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
import pdb # @DEBUG
#import cProfile # @DEBUG
import timeit # @DEBUG

from Board import Board, Stage
from AgentController import AgentController
from HandScanner import HandScanner

NUM_AGENTS = 2;

def printHelp():
    pass;

def makeGame():
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
    numAgents = NUM_AGENTS;
    agents = [AgentController() for i in range(numAgents)];

    # Create the board
    board = Board();

    # Start with a minimum bet, ante-like
    board.setBet(5);
    board.setPot(500 * NUM_AGENTS);

    # Draw a hand for each agent
    [agent.drawHand(board) for agent in agents];

    # And the game loop. This is done as long as there is more than one agent in the game, and we are not finished with the final betting round
    while([agent.inGame() for agent in agents].count(True) > 1 and board.getStage() != Stage.SHOWDOWN):
        # Make their decision
        for agent in agents:
            if(agent.inGame()):
                print("Agent",agents.index(agent),"choosing...");
                agent.makeDecision(board)
                if(not agent.inGame() and not [agent.inGame() for agent in agents].count(True) > 1):
                    print("Agent",[agents.index(agent) for agent in agents if agent.inGame()][0],"wins by default");
                    break;

        # Change the stage
        board.setStage(board.getStage().nextStage());
        print("Stage:",board.getStage());

    # One winner or in showdown
    if(board.getStage() == Stage.SHOWDOWN):
        hands = [agent.getHand() for agent in agents if agent.inGame()];
        winnerIndex = HandScanner().declareWinner(hands, board);
        
        if(type(winnerIndex) == int):
            winner = winnerIndex;
        elif(type(winnerIndex) == list):
            if(len(winnerIndex) == 1):
                winner = winnerIndex[0];
            else:
                winner = winnerIndex;
        print("Winner: agent",winner);
        return winner;

    elif([agent.inGame() for agent in agents].count(True) == 1): # If we only have one agent which is still in the game...
        winnerIndex = agents.index([agent for agent in agents if agent.inGame()][0]);
        print("Winner: agent",winnerIndex);

    else:
        print("You shouldn't be here, as the game loop exited too early. Exiting...");
        sys.exit(401);

if __name__ == '__main__':
    #makeGame();
    #cProfile.run('makeGame()');
    timer = timeit.timeit(stmt="makeGame()", setup="from __main__ import makeGame", number=100);
    print("Time over 100 iterations:",timer);
    print("Average time per iteration:",timer/100);
