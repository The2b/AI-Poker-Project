#!/usr/bin/python3

'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 28 February 2018
@project Texas Hold'em AI
@file HandOddsWorkerKernel.py
'''

'''
Welp, break's over! This is a modified version of scanner-checker.py
I'm using it for a couple of things.
    1) To play around with the super computer and distributed programming
    2) To see if Python's RNG is significantly different from what it should be
    3) To gather data on odds so I don't need to do it myself
'''

from handScanner import HandScanner, HandIDs
from board import Board, Stage
from card import Card
from deck import Deck

import WorkerFunctions

import rpyc # RPC connections
from rpyc.utils.server import ThreadedServer

import time # File naming, timing
import multiprocessing as mp

class HandOddsWorkerService(rpyc.Service):
    __NUM_HANDS = 10;
    __BATCH_SIZE = 100000;
    __PROCESS_COUNT = 12;
    processList = [];
    totalList = [0 for i in range(__NUM_HANDS)];
    queue = mp.Queue();

    def exposed_startProcesses(self):
        self.processList = [mp.Process(target=WorkerFunctions.playSet,args=(self.__BATCH_SIZE,self.queue,)) for i in range(self.__PROCESS_COUNT)];

        for process in self.processList:
            process.start();

    def exposed_killProcesses(self):
        print("Closing children...");
        for process in self.processList:
            process.terminate();

        print("Children closed");
        self.processList = [];
        return;

    def exposed_submitQueue(self, maximum=50000):
        count = 0;
        try:
            while(count < maximum):
                self.totalList[self.queue.get().value] += 1;
                count += 1;
        finally:
            return count;

    def exposed_getQueue(self):
        return self.queue;

    def exposed_getTotalList(self, queue):
        queue.put(self.totalList);

    def exposed_setBatchSize(self,size):
        self.__BATCH_SIZE = size;

    def exposed_setProcessCount(self,count):
        self.__PROCESS_COUNT = count;

    def on_connect(self):
        self.exposed_totalList = [0,0,0,0,0,0,0,0,0,0];
    
    def on_disconnect(self):
        print("Disconnecting...");
        self.exposed_killProcesses();

if __name__ == "__main__":
    startTime = time.time();

    try:
        workerPort = os.environ['TL_WORKER_PORT'];
        assert workerPort != None;
        assert type(int(workerPort)) == int;
        assert workerPort > 0;
        assert workerPort < 65536;
    except:
        workerPort = 18661;

    t = ThreadedServer(HandOddsWorkerService,port=workerPort);
    t.start();
