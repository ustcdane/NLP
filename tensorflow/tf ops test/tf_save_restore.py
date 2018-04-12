import tensorflow as tf
import numpy as np

v1 = tf.Variable(tf.zeros([2]), name='bias')

saver = tf.train.Saver({"my_v1":v1})

x = [0,0]
# save 
with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	print sess.run([v1],feed_dict={v1:x})
	save_path = saver.save(sess, 'model_save_tmp/model.ckpt')
	print 'save model ', save_path

# restore variables from disk
with tf.Session() as sess:
	saver.restore(sess, 'model_save_tmp/model.ckpt')
	print 'Model restored.'
	print 'v1:', sess.run(v1)

