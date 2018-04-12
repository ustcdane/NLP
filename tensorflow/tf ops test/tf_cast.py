import tensorflow as tf

t = tf.cast(True, dtype=tf.float32)
f = tf.cast(False, dtype=tf.float32)
with tf.Session() as sess:
	t_, f_ = sess.run([t,f])
	print t_, f_
