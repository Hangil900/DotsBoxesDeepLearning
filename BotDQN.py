import config
import tensorflow as tf
import tensorflow.contrib.slim as slim
from Qnetwork import Qnetwork
import pdb
import random
import numpy as np

class BotDQN:
    def __init__(self, board, playerNum):
        self.board = board

        h_size = config.DQN_h_size
        width = config.DQN_width
        height = config.DQN_height
        num_actions = config.DQN_state_size

        tf.reset_default_graph()
        self.mainQN = Qnetwork(h_size, width, height, num_actions)

        self.init = tf.global_variables_initializer()
        
        self.saver = tf.train.Saver()

        self.sess = tf.Session()
        self.sess.run(self.init)

        ckpt = tf.train.get_checkpoint_state(config.DQN_path)
        self.saver.restore(self.sess,ckpt.model_checkpoint_path)


    def action_space_sample(self):
        print "Random move!"
        num_left = len(self.board.empty_states)
        ind = int(random.random() * num_left)

        for action in self.board.empty_states:
            if ind == 0:
                return action
            else:
              ind -= 1

        
    def getNextMove(self, gameGUI):
        s = self.board.board_state
        a, Qout = self.sess.run([self.mainQN.predict,self.mainQN.Qout],
                                feed_dict={self.mainQN.imageIn:[s]})
        Qout *= -1
        actions = np.argsort(Qout).flatten()
        for i in range(len(actions)):
            a = actions[i]
            if a in self.board.empty_states:
                move = self.board.state_to_move[a]
                return move
            
    

        
