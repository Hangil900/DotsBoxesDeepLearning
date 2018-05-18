# coding: utf-8
import tensorflow as tf
import numpy as np
from ConvNet import ConvNet
path = './model_soobin'
model_name = '/soobin-1-4900'

class BotConvNet:
    def __init__(self, board, playerNum):
        self.board = board
        assert self.board.width == self.board.height and self.board.width == 5
        self.board_size = self.board.width

        # tf.reset_default_graph()
        # self.mainQN = ConvNet(self.board_size)

        # self.init = tf.global_variables_initializer()
        
        # self.saver = tf.train.Saver()

        # self.sess = tf.Session()
        # self.sess.run(self.init)

        # ckpt = tf.train.latest_checkpoint(path)
        # print "Restoring " + str(ckpt)
        # self.saver.restore(self.sess,ckpt)



        init = tf.global_variables_initializer()
        self.mainQN = ConvNet(self.board_size)
        self.sess = tf.Session()
        self.sess.run(init)
        saver = tf.train.Saver()

        ckpt = tf.train.latest_checkpoint('./model_soobin')
        print "Restoring " + str(ckpt)
        saver.restore(self.sess, ckpt)

        # print([node.name for node in tf.get_default_graph().as_graph_def().node])

    def state_to_input_volume(self, state):
        board_size = self.board.width
        rtn = np.zeros(np.power((2 * board_size - 1), 2))
        for i, value in enumerate(state):
            rtn[2 * i + 1] = value
        rtn_reshaped = rtn.reshape((2 * board_size - 1, 2 * board_size - 1))
        rtn_reshaped = rtn_reshaped.reshape([-1, 2 * board_size - 1, 2 * board_size - 1, 1])
        return rtn_reshaped

    # def output_to_state(self, output):
    #     output = np.reshape(output, -1)
    #     rtn = np.zeros(board_array_size)
    #     for i, value in enumerate(output):
    #         if i % 2 == 1:
    #             rtn[(i-1) / 2] = value
    #     return rtn

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
        s = self.board.board_state[0]
        print s
        s = self.state_to_input_volume(s)
        Qout = self.sess.run([self.mainQN.Qout], feed_dict={self.mainQN.input: s})[0]
        Qout *= -1
        actions = np.argsort(Qout).flatten()
        for i in range(len(actions)):
            a = actions[i]
            if a in self.board.empty_states:
                print "choosing a move!"
                move = self.board.state_to_move[a]
                print move
                return move

