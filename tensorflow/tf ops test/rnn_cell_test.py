import tensorflow as tf
import os
#https://github.com/tensorflow/tensorflow/blob/r1.7/tensorflow/python/ops/rnn_cell_impl.py
os.environ['CUDA_VISIBLE_DEVICES'] = ''
 

print '*'*20
print 'BasicRNNCell'
 
cell = tf.nn.rnn_cell.BasicRNNCell(num_units=128)
print(cell.state_size)
inputs = tf.placeholder(tf.float32, shape=[32, 100])
h0 = cell.zero_state(32, tf.float32)
print "h0 shape:", h0.shape
output, h1 = cell(inputs=inputs, state=h0)
print(output, output.shape)
print(h1, h1.shape)


print '*'*20
print 'BasicLSTMCell'
cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=128)
print(cell.state_size)
inputs = tf.placeholder(tf.float32, shape=(32, 100))
h0 = cell.zero_state(32, tf.float32)
print 'h0:', h0
print "h0 is a LSTMStateTuple (c,h).", " c shape:", h0.c.shape, "h shape:", h0.h.shape
output, h1 = cell(inputs=inputs, state=h0)
print'h1:', h1
print "h1.h", h1.h, h1.h.shape
print "h1.c:", h1.c, h1.c.shape
print "output:",output, output.shape
