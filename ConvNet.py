import numpy as np
import random
import tensorflow as tf

class ConvNet:
    def __init__(self, board_size):
        self.session = tf.Session()
        num_moves = (2 * board_size - 1) * (board_size - 1) + board_size - 1
        # Two conv + relu + max_pool layers
        self.input = tf.placeholder(shape=[1, 2 * board_size - 1, 2 * board_size - 1, 1], dtype=tf.float32)
        layer1 = self.create_new_conv_layer(input_data = self.input, 
                                            num_input_channels = 1, 
                                            num_filters = 32, 
                                            filter_shape = [3, 3], 
                                            pool_shape = [2, 2], 
                                            name='layer1')
        layer2 = self.create_new_conv_layer(input_data = layer1, 
                                            num_input_channels = 32, 
                                            num_filters = 64, 
                                            filter_shape = [5, 5], 
                                            pool_shape = [2, 2], 
                                            name='layer2')
        flattened = tf.reshape(layer2, [-1, 3 * 3 * 64])
                
        # setup some weights and bias values for this layer, then activate with ReLU
        wd1 = tf.Variable(tf.truncated_normal([3 * 3 * 64, 1000], stddev=0.03), name='wd1')
        bd1 = tf.Variable(tf.truncated_normal([1000], stddev=0.01), name='bd1')
        dense_layer1 = tf.matmul(flattened, wd1) + bd1
        dense_layer1 = tf.nn.relu(dense_layer1)
        
        # another layer with softmax activations
        wd2 = tf.Variable(tf.truncated_normal([1000, num_moves], stddev=0.03), name='wd2')
        bd2 = tf.Variable(tf.truncated_normal([num_moves], stddev=0.01), name='bd2')
        self.Qout = tf.matmul(dense_layer1, wd2) + bd2
        self.predict = tf.argmax(self.Qout, 1)
        
        # Loss
        self.nextQ = tf.placeholder(shape=[1, (2 * board_size - 1) * (board_size - 1) + board_size - 1], dtype=tf.float32)
        # cross_entropy
#         self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.Qout, labels=self.nextQ))       
#         self.updateModel = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(self.loss)
        
        self.td_error = tf.square(self.Qout - self.nextQ)
        self.loss = tf.reduce_mean(self.td_error)
        self.trainer = tf.train.AdamOptimizer(learning_rate=0.0001)
        self.updateModel = self.trainer.minimize(self.loss)
        
    def create_new_conv_layer(self, input_data, num_input_channels, num_filters, filter_shape, pool_shape, name):
        # setup the filter input shape for tf.nn.conv_2d
        conv_filt_shape = [filter_shape[0], filter_shape[1], num_input_channels,
                          num_filters]
        
        # initialise weights and bias for the filter
        weights = tf.Variable(tf.truncated_normal(conv_filt_shape, stddev=0.03),
                                          name=name+'_W')
        bias = tf.Variable(tf.truncated_normal([num_filters]), name=name+'_b')

        # setup the convolutional layer operation
        out_layer = tf.nn.conv2d(input_data, weights, [1, 1, 1, 1], padding='SAME')

        # add the bias
        out_layer += bias

        # apply a ReLU non-linear activation
        out_layer = tf.nn.relu(out_layer)

        # now perform max pooling
        ksize = [1, pool_shape[0], pool_shape[1], 1]
        strides = [1, 2, 2, 1]
        out_layer = tf.nn.max_pool(out_layer, ksize=ksize, strides=strides, 
                                   padding='SAME')

        return out_layer
    
    def get_session(self):
        return self.session
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close() 
        
    