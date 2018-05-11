import tensorflow as tf
import os

os.environ['CUDA_VISIBLE_DEVICES'] = ''

with tf.name_scope("hehe"):
    input_param = tf.get_variable('w2', shape=[96, 512])
    input_param_flat = tf.reshape(input_param, [-1])
    input_reshape = tf.reshape(input_param, [-1,64])
    print tf.shape(input_param)
    print tf.shape(input_param_flat)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    in_, in_flat, in_re = sess.run([input_param, input_param_flat, input_reshape])
    print in_.shape
    print in_flat.shape
    print in_re.shape
