#!/usr/bin/env/python
# coding=utf-8
import tensorflow as tf
import numpy as np

input_ids = tf.placeholder(dtype=tf.int32, shape=[None])

embedding = tf.Variable(np.identity(5, dtype=np.int32))
input_embedding = tf.nn.embedding_lookup(embedding, input_ids)

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())
print(embedding.eval())
print(sess.run(input_embedding, feed_dict={input_ids:[1, 2, 3, 0, 3, 2, 1]}))