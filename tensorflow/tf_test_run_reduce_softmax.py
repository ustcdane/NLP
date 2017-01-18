import numpy as np
import tensorflow as tf
#from tensorflow.examples.tutorials.mnist import input_data
import os

#x = tf.placeholder(tf.float32, shape=[None, 784],name = "Image")
#y_ = tf.placeholder(tf.float32, shape=[None, 10],name = "Correct_Image_label")
#print type(x)
#Reshaping the input for convnet
#x_image = tf.reshape(x, [-1,28,28,1],name = "Reshaped_Image")


init_op = tf.initialize_all_variables()

x = tf.placeholder(tf.float32, shape=(2, 2))
y = tf.matmul(x, x)
y2Times = x + x

#reduce test
reduce_mean = tf.reduce_mean(x, 1)

# softmax test
x_ = tf.placeholder(tf.float32, shape=(1, 2))
W = tf.Variable(tf.zeros([2,2]))
b = tf.Variable(tf.zeros([2]))

ySoft = tf.nn.softmax(tf.matmul(x_, W) + b)

with tf.Session() as sess:
    #print(sess.run(y))  # ERROR: will fail because x was not fed.
    sess.run(init_op)
    #rand_array = np.random.rand(2, 2)
    test_array = np.array([[1.,1.,],[2.,2.]])
    print "x:\n", test_array
    y_, y2Times_, reduce_mean_= sess.run([y, y2Times, reduce_mean], feed_dict={x: test_array})
    print 'x*x:\n', y_
    print 'x+x:\n', y2Times_
    print 'tf.reduce_mean(x, 1):\n', reduce_mean_
    print '\nsoftmax test:'
    x_in = np.array([[1,1]])
    w_in = np.array([[0,1],[1,1]])
    b_in = np.array([0,0])
    print 'x:\n', x_in
    print 'W:\n', w_in
    print 'b:\n', b_in
    res = sess.run([ySoft], feed_dict={x_:x_in, W:w_in, b:b_in})
    print 'tf.nn.softmax(tf.matmul(x_in, w_in) + b_in)', res