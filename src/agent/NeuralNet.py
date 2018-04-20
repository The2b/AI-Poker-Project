from __future__ import absolute_import, division, print_function
'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 14 April 2018
@project Texas Hold'em AI
@file NeuralNet.py
'''

'''
This will create a dense neural net with the following features:
    Amount of money the agent had at the start
    Amount of money the opponent had at the start
    Old pot value
    LastAgentAction
    LastOppoAction
    Old bet amount
    New bet amount
    Agent's hand 1
    Agent's hand 2
    Community Pool 1
    Community Pool 2
    Community Pool 3
    Community Pool 4
    Community Pool 5
    Agent's win chance from agent's view
    Opponent win chance from agent's view
    Tie chance from agent's view
    Stage of the game
    # cards left in the deck

I may later add the number of cards left to show, but that's not in there atm
I may also add something for how much money the agent and opponent have in the pool already that hand

We want to predict the action a certain bet will cause from the opponent
Actions are enumerated as follows:
    CALL:0
    RAISE:1
    FOLD:2
'''

import tensorflow as tf
import tensorflow.contrib.eager as tfe
import matplotlib.pyplot as plt
import numpy as np
import os
import pdb

class NeuralNet:
    model = 0;
    modelData = 0;
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0001);
    quiet = False;

    def __init__(self, csvPath="/home/the2b/Documents/school/ai/project/src/test6.csv", dataUrl="http://127.0.0.1/test6.csv", epochs=501, skip=2, train=True, quiet=False):
        try:
            tf.enable_eager_execution();
        except ValueError: # In case we're already running eagerly
            pass;


        self.quiet = quiet;

        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(152, activation="relu", input_shape=(19,)),
            tf.keras.layers.Dense(76, activation="relu"),
            tf.keras.layers.Dense(38, activation="relu"),
            tf.keras.layers.Dense(19, activation="relu"),
            tf.keras.layers.Dense(3) # 0 being call, 1 being raise, 2 being fold
        ]);

        self.modelData = self.getDataSet(csvPath,dataUrl,batchSize=64);
        if(train):
            self.trainModel(epochs=epochs);

    def parse_csv(self, line):
        example_defaults = [[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0]]  # sets field types
        parsed_line = tf.decode_csv(line, example_defaults, na_value="nan")
        
        # First 19 fields are features, combine into single tensor
        features = tf.reshape(parsed_line[:-1], shape=(19,))
        # Last field is the label
        label = tf.reshape(parsed_line[-1], shape=(1,))

        return features, label


    def setLearningRate(self, learningRate):
        self.optimizer._learning_rate = learningRate;
        return;

    def getDataSet(self, fpath, url, batchSize=32, skip=2):
        test_fp = tf.keras.utils.get_file(fname=os.path.basename(fpath), origin=url);
        train_dataset = tf.data.TextLineDataset(test_fp);
        
        train_dataset = train_dataset.skip(skip); # Skip header and descriptor
        train_dataset = train_dataset.map(self.parse_csv);
        train_dataset = train_dataset.shuffle(buffer_size=1000);
        train_dataset = train_dataset.batch(batchSize);
        #print(train_dataset);
        #print("train_dataset:",train_dataset);
        return train_dataset;

    '''
    data can be a path to a CSV file or a Dataset
    '''
    def addDataToModel(self, data, bufferSize=1000, batchSize=32):
        #print("Weights before change:", self.model.get_weights());
        print("Adding new data to model...");
        if(type(data) == str):
            try:
                newDataset = tf.data.TextLineDataset(csvPath);
                newDataset = newDataset.skip(2);
                newDataset = newDataset.map(self.parse_csv);
            except:
                print("ERROR: Could not read new csv file into opponent model");
        elif(isinstance(data, tf.data.Dataset)):
            newDataset = data;

        else:
            print("Type of data:",type(data));
            return;

        self.trainModel(data=newDataset, batchSize=1, bufferSize=bufferSize);
        #print("Weights after change:", self.model.get_weights());

    def loss(self, x, y):
        y_ = self.model(x);
        return tf.losses.sparse_softmax_cross_entropy(labels=y, logits=y_);

    def grad(self, inputs, targets): # Try using maximum return as target?
        with tfe.GradientTape() as tape:
            loss_value = self.loss(inputs, targets)
        return tape.gradient(loss_value, self.model.variables)

    def trainModel(self, data=0, epochs=501, batchSize=32, bufferSize=1000):
        train_loss_results = []
        train_accuracy_results = []

        if(data == 0):
            trainingData = self.modelData;

        else:
            trainingData = data;
            trainingData = trainingData.shuffle(buffer_size=bufferSize);
            trainingData = trainingData.batch(batch_size=batchSize);

        num_epochs = epochs;

        for epoch in range(num_epochs):
            epoch_loss_avg = tfe.metrics.Mean()
            epoch_accuracy = tfe.metrics.Accuracy()

            # Training loop - using batches of 32
            for x, y in tfe.Iterator(trainingData):
                # Optimize the model
                grads = self.grad(x, y)
                self.optimizer.apply_gradients(zip(grads, self.model.variables),global_step=tf.train.get_or_create_global_step())

                epoch_loss_avg(self.loss(x, y))  # add current batch loss
                # compare predicted label to actual label
                epoch_accuracy(tf.argmax(self.model(x), axis=1, output_type=tf.int32), y)

            # end epoch
            train_loss_results.append(epoch_loss_avg.result())
            train_accuracy_results.append(epoch_accuracy.result())

            if((epoch % 50 == 0) and not self.quiet):
                print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,epoch_loss_avg.result(),epoch_accuracy.result()))
            if(self.optimizer._learning_rate == 0.0001):
                if(epoch == 100):
                    self.setLearningRate(0.001);
                if(epoch == 250):
                    self.setLearningRate(0.01);
                if(epoch == 500):
                    self.setLearningRate(0.1);

        #print("Model weights after training",self.model.get_weights());

        return [train_loss_results, train_accuracy_results];

    def plotStats(self, train_loss_results, train_accuracy_results):
        fig, axes = plt.subplots(2, sharex=True, figsize=(12, 8))
        fig.suptitle('Training Metrics - Call, Raise, or Fold')

        axes[0].set_ylabel("Loss", fontsize=14)
        axes[0].plot(train_loss_results)

        axes[1].set_ylabel("Accuracy", fontsize=14)
        axes[1].set_xlabel("Epoch", fontsize=14)
        axes[1].plot(train_accuracy_results)

        plt.show()

if __name__ == '__main__':
    import tensorflow as tf
    import NeuralNet

    #pdb.set_trace();
    tf.enable_eager_execution();
    net = NeuralNet.NeuralNet(train=False, csvPath="/home/the2b/Documents/school/ai/project/src/test6.csv", dataUrl="http://127.0.0.1/test6.csv");
    trainingRes = net.trainModel(epochs=501, batchSize=72, bufferSize=10000);
    net.plotStats(trainingRes[0], trainingRes[1]);
