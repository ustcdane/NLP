import tensorflow as tf
import random
tf.set_random_seed(777)  # for reproducibility
import numpy as np
import os
import pdb
os.environ['CUDA_VISIBLE_DEVICES'] = ''
#config = tf.ConfigProto()

## inputs tensor
x = tf.placeholder(tf.int32, [None, None], name='x')  # sentence
### look_up 
vocabulary_size=10
embedding_size = 2
w_embed = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0), name='w_embed')

# inputs em
inputs_embed = tf.nn.embedding_lookup(w_embed, x)

# input xx real data
batch_size=4
sequence_length=5
xx=np.zeros((batch_size, sequence_length),dtype=np.int32)
xx[0][:1] = 1
xx[1][:2] = 2
xx[2][:3] = 3 
xx[3][:4] = 4 
x_len=np.array([1,2,3,4])


#lstm_cell = tf.nn.rnn_cell.LSTMCell(4)
# create 2 LSTMCells hidden size 4, 2
rnn_layers = [tf.nn.rnn_cell.LSTMCell(size) for size in [4,2]]
# create a RNN cell composed sequentially of a number of RNNCells
multi_rnn_cell = tf.nn.rnn_cell.MultiRNNCell(rnn_layers)
# 'state' is a N-tuple where N is the number of LSTMCells containing a
# tf.contrib.rnn.LSTMStateTuple for each cell (N-tuple hidden state)
# state = [LSTMStateTuple(c1,h1),LSTMStateTuple(c2,h2),LSTMStateTuple(c3,h3).... 
outputs, state = tf.nn.dynamic_rnn(cell=multi_rnn_cell,inputs=inputs_embed, sequence_length=x_len,dtype=tf.float32)
final_state = state[-1] # final hidden state
final_state_h = state[-1].h
final_state_c = state[-1].c

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	print 'input shape:\n', xx.shape
	print 'input xx:\n', xx
	em, out, st, f_st, f_st_h= sess.run([inputs_embed, outputs, state, final_state, final_state_h], feed_dict={x:xx})
	print 'input embedding shape:', em.shape
	print 'input embedding:\n', em
	
	print 'outputs shape:', out.shape
	print 'outputs:\n', out
	
	print 'state shape:', type(st)
	print 'state:\n', st
	
	print 'state[-1] shape:', type(f_st)
	print 'state[-1]:\n', f_st
	
	print 'state[-1].h:', f_st_h.shape
	print 'state[-1].h:\n', f_st_h
