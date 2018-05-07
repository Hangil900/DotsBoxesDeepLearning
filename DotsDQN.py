
# coding: utf-8

# # Simple Reinforcement Learning with Tensorflow Part 4: Deep Q-Networks and Beyond
# 
# In this iPython notebook I implement a Deep Q-Network using both Double DQN and Dueling DQN. The agent learn to solve a navigation task in a basic grid world. To learn more, read here: https://medium.com/p/8438a3e2b8df
# 
# For more reinforcment learning tutorials, see:
# https://github.com/awjuliani/DeepRL-Agents

# In[1]:

from __future__ import division

import numpy as np
import random
import tensorflow as tf
import tensorflow.contrib.slim as slim
import matplotlib.pyplot as plt
import scipy.misc
import os, config

import time
from Qnetwork import Qnetwork


# ### Load the game environment

# Feel free to adjust the size of the gridworld. Making it smaller provides an easier task for our DQN agent, while making the world larger increases the challenge.

# In[2]:
import environment, board


# Above is an example of a starting environment in our simple game. The agent controls the blue square, and can move up, down, left, or right. The goal is to move to the green square (for +1 reward) and avoid the red square (for -1 reward). The position of the three blocks is randomized every episode.

# ### Implementing the network itself

# In[3]:

# ### Experience Replay

# This class allows us to store experies and sample then randomly to train the network.

# In[4]:

class experience_buffer():
    def __init__(self, buffer_size = 50000):
        self.buffer = []
        self.buffer_size = buffer_size
    
    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)
            
    def sample(self,size):
        return np.reshape(np.array(random.sample(self.buffer,size)),[size,5])


# These functions allow us to update the parameters of our target network with those of the primary network.

# In[6]:

def updateTargetGraph(tfVars,tau):
    total_vars = len(tfVars)
    op_holder = []
    for idx,var in enumerate(tfVars[0:total_vars//2]):
        op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
    return op_holder

def updateTarget(op_holder,sess):
    for op in op_holder:
        sess.run(op)


def processState(states):
    return states
    return np.reshape(states,[21168])

def get_wanted_action(Qout, env):
    actions = np.argsort(Qout).flatten()
    
    if config.DQN_handle_invalid_moves:
        for i in range(len(actions)):
            a = actions[i]
            if a in env.board.empty_states:
                break
        return a
    else:
        return actions[0]


# ### Training the network

# Setting all the training parameters

# In[7]:

size = config.DQN_width
width = config.DQN_width
height = config.DQN_height
board_size = height + width -1

env = environment.Environment(size)
num_actions = env.board_state_size

batch_size = config.DQN_batch_size #How many experiences to use for each training step.
#batch_size = 2
update_freq = config.DQN_update_freq #How often to perform a training step.
y = .99 #Discount factor on the target Q-values
startE = 1 #Starting chance of random action
endE = 0.1 #Final chance of random action
annealing_steps = 10000. #How many steps of training to reduce startE to endE.
num_episodes = config.DQN_num_episodes #How many episodes of game environment to train network with.
pre_train_steps = config.DQN_pre_train_steps #How many steps of random actions before training begins.
max_epLength = width * height*4  #The max allowed length of our episode.
load_model = False #Whether to load a saved model.
path = config.DQN_path #The path to save our model to.
h_size = config.DQN_h_size #The size of the final convolutional layer before splitting it into Advantage and Value streams.
tau = 0.001 #Rate to update target network toward primary network


# In[ ]:

tf.reset_default_graph()
mainQN = Qnetwork(h_size, width, height, num_actions)
targetQN = Qnetwork(h_size, width, height, num_actions)

init = tf.global_variables_initializer()

saver = tf.train.Saver()

trainables = tf.trainable_variables()

targetOps = updateTargetGraph(trainables,tau)

myBuffer = experience_buffer()

#Set the rate of random action decrease. 
e = startE
stepDrop = (startE - endE)/annealing_steps

#create lists to contain total rewards and steps per episode
jList = []
rList = []
total_steps = 0

#Make a path for our model to be saved in.
if not os.path.exists(path):
    os.makedirs(path)

start = time.time()
log_file_path = config.DQN_path + "_log.txt"
log_file = open(log_file_path, 'wb')
log_file.write("Episode #, # of steps, Avg Score, e\n")

with tf.Session() as sess:
    sess.run(init)
    if load_model == True:
        print('Loading Model...')
        ckpt = tf.train.get_checkpoint_state(path)
        saver.restore(sess,ckpt.model_checkpoint_path)
    for i in range(num_episodes):
        episodeBuffer = experience_buffer()
        #Reset environment and get first new observation
        s = env.reset()
        s = processState(s)
        d = -1 # -1: not finished, 0: invalid move, 1: finished
        rAll = 0
        j = 0
        #The Q-Network
        while j < max_epLength:
            #If the agent takes longer than 200 moves to reach either
            # of the blocks, end the trial.
            j+=1
            #Choose an action by greedily (with e chance of random action)
            # from the Q-network
            if np.random.rand(1) < e or total_steps < pre_train_steps:
                if config.DQN_use_minimax_moves:
                    a = env.get_minimax_move()
                else:
                    a = env.action_space_sample()
            else:
                Qout = sess.run(mainQN.Qout,feed_dict={mainQN.imageIn:[s]})
                a= get_wanted_action(Qout, env)
                
            s1,r,d = env.step(a)
            s1 = processState(s1)
            total_steps += 1
            #Save the experience to our episode buffer.
            episodeBuffer.add(np.reshape(np.array([s,a,r,s1,d]),[1,5])) 
            
            if total_steps > pre_train_steps:
                if e > endE:
                    e -= stepDrop
                
                if total_steps % (update_freq) == 0:
                    #Get a random batch of experiences.
                    trainBatch = myBuffer.sample(batch_size)

                    imageIn = np.vstack(trainBatch[:, 3]).reshape((-1, board_size,
                                                                   board_size, 3))
                    
                    #Below we perform the Double-DQN update to the target Q-values
                    Q1 = sess.run(mainQN.predict,
                                     feed_dict={mainQN.imageIn:imageIn})

                    imageIn = np.vstack(trainBatch[:, 3]).reshape((-1, board_size,
                                                                   board_size, 3))
                    Q2 = sess.run(targetQN.Qout,
                                  feed_dict={targetQN.imageIn:imageIn})
                    
                    end_multiplier = -(trainBatch[:,4] - 1)
                    doubleQ = Q2[range(batch_size),Q1]
                    targetQ = trainBatch[:,2] + (y*doubleQ * end_multiplier)
                    #Update the network with our target values.

                    imageIn = np.vstack(trainBatch[:,0]).reshape((-1, board_size,
                                                                  board_size, 3))
                    _ = sess.run(mainQN.updateModel,
                                 feed_dict={mainQN.imageIn: imageIn,
                                            mainQN.targetQ:targetQ,
                                            mainQN.actions:trainBatch[:,1]})
                    
                    #Update the target network toward the primary network.
                    updateTarget(targetOps,sess)

            if d != 0:
                # Only add rewards that weren't because of wrong move.
                rAll += r
                
            s = s1
            
            if d == True:
                break
        
        myBuffer.add(episodeBuffer.buffer)
        jList.append(j)
        rList.append(rAll)
        #Periodically save the model. 
        if i % 1000 == 0:
            saver.save(sess,path+'/model-'+str(i)+'.ckpt')
            print("Saved Model")
        if len(rList) % 10 == 0:
            line = "{0}, {1}, {2}, {3}\n"
            line = line.format(len(rList), total_steps, np.mean(rList[-10:]), e)
            print line
            log_file.write(line)

        if len(rList) % 100 == 0:
            end = time.time()
            mins = round((end - start) / 60.0, 1)
            eps = len(rList)
            print "Eps: {0}, Time: {1}".format(eps, mins)
            
    saver.save(sess,path+'/model-'+str(i)+'.ckpt')
#print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")


# ### Checking network learning

# Mean reward over time

# In[ ]:
log_file.close()
rList = np.array(rList)

wins = rList > 0

print("Percent of success: " + str(sum(wins)/ float(num_episodes)) + "%")
plt.plot(rList, 'r--')


# In[ ]:



