import tensorflow as tf

with tf.name_scope("hehe"):
	w1 = tf.Variable(1.0)
	w2 = tf.get_variable('w2', shape=[1])
	with tf.variable_scope("var1",reuse=tf.AUTO_REUSE):
		 w3 = tf.get_variable("w3",shape=[2])
		 w4 = tf.Variable(2.0)
		 print tf.get_variable_scope().reuse
		 #tf.get_variable_scope().reuse_variables()
		 #print tf.get_variable_scope().reuse
		 ww = tf.get_variable('w3')
		 #print tf.get_variable_scope().reuse
		 ww2 = tf.get_variable('w4', shape=[2])
		 print ww
print w1.name
print w2.name
print w3.name
print w4.name

print ww.name
print ww2.name
