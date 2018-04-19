'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 01 March 2018
@project Texas Hold'em AI
@file HandOddsWorkerKernel.py
'''

'''
This is the kernel for the worker nodes to generate a list of hands.
Look at the Master kernel for more info.
'''

import rpyc # Duh
import os # environ
import time # File naming, timing
import sys # exit
import signal # cleanup

import ipArgParser

__ITERATIONS = 10000000; # @TODO make this available as an arg
__BATCH_SIZE = 10000;
__PROCESS_COUNT = 12;
__NUM_HANDS = 10;
runsCompleted = 0;
connList = [];

def printReport(runsCompleted, totalResults, startTime, endTime):
    totalResultsP = [100*(res/runsCompleted) for res in totalResults];

    # Format our report
    formattedStr = \
"Hands played: {}\n\
\n\
High Cards: {}\n\
Pairs: {}\n\
Two Pairs: {}\n\
Three of a Kind: {}\n\
Straight: {}\n\
Flush: {}\n\
Full House: {}\n\
Four of a Kind: {}\n\
Straight Flush: {}\n\
Five of a Kind: {}\n\
\n\
High Card Percentage: {:.3f}%\n\
Pair Percentage: {:.3f}%\n\
Two Pair Percentage: {:.3f}%\n\
Three of a Kind Percentage: {:.3f}%\n\
Straight Percentage: {:.3f}%\n\
Flush Percentage: {:.3f}%\n\
Full House Percentage: {:.3f}%\n\
Four of a Kind Percentage: {:.3f}%\n\
Straight Flush Percentage: {:.3f}%\n\
Five of a Kind Percentage: {:.3f}%\n\
\n\
Start time: {}\n\
End time: {}\n\
Total time spent: {} seconds\n".format(runsCompleted, totalResults[0], totalResults[1], totalResults[2], totalResults[3], totalResults[4], totalResults[5], totalResults[6], totalResults[7], totalResults[8], totalResults[9], totalResultsP[0], totalResultsP[1], totalResultsP[2], totalResultsP[3], totalResultsP[4], totalResultsP[5], totalResultsP[6], totalResultsP[7], totalResultsP[8], totalResultsP[9], time.strftime("%c",time.localtime(startTime)), time.strftime("%c",time.localtime(endTime)),endTime-startTime);

    print(formattedStr);

    # Write our report to a file, print it to the console
    fileName = time.strftime("%Y-%m-%d-%H-%M-%S-texas-holdem.report",time.localtime());
    fileStream = open(fileName,'w');

    print("Writing report to file {}".format(fileName));

    fileStream.write(formattedStr);
    fileStream.close();

def cleanup(signum, frame):
    # Finally, close and kill the servers
    for conn in connList:
        conn.root.exposed_killProcesses();
        conn.close();

    sys.exit(0);

if __name__ == '__main__':
    # Create the connection to the worker nodes
    # Because Dr. Perry asked me not to share the IPs, and this is going on GitHub, I'll configure it via arguments
    ipList = ipArgParser.getArgIPs(sys.argv);
    assert ipList != None;
    #print(ipList);

    # And override the port w/ TL_WORKER_PORT
    try:
        port = os.environ['TL_WORKER_PORT'];
        assert port != None;

    except:
        port = 18661;

    # Connect to the worker nodes
    connList = [rpyc.connect(node,port) for node in ipList];

    signal.signal(signal.SIGINT, cleanup);
    
    funcList = [];
    promiseList = [None for n in range(len(connList))];

    startTime = time.time();

    # PREP WORK BITCHES!!
    for conn in connList:
        funcList.append(rpyc.async(conn.root.exposed_submitQueue));
        conn.root.exposed_setProcessCount(__PROCESS_COUNT);
        conn.root.exposed_setBatchSize(__BATCH_SIZE);
        conn.root.exposed_startProcesses();

    # DO IT!!
    while(runsCompleted < __ITERATIONS):
        for conn in connList:
           index = connList.index(conn);
           promise = promiseList[index];
           asyncFunc = funcList[index];
           try:
               isReady = promise.ready; # So we don't overwrite a set of values because they became ready between calls
           except:
               isReady = False;

           if(isReady):
               print("Node {} becomes ready...".format(index));
               runsCompleted += promise.value;

           if(isReady or promise == None):
               print("Moving {} jobs from node {}'s buffer to total".format(__BATCH_SIZE,index));
               print(runsCompleted,"jobs done.");
               promiseList[index] = asyncFunc(__BATCH_SIZE);

    # Get and tally our results
    resQueue = mp.Queue();
    resList = [0 for i in range(__NUM_HANDS)];
    for conn in connList:
        for index in range(__NUM_HANDS):
            conn.root.exposed_getTotalList(resQueue);
            connTotal = resQueue.get();
            resList[index] += connTotal[index];

    endTime = time.time();

    print("End time: ",endTime);

    printReport(sum(resList),resList,startTime, endTime);

