import tensorflow as tf
import numpy as np
import os

#https://www.tensorflow.org/api_guides/python/train#Gradient_Clipping
#https://www.tensorflow.org/api_docs/python/tf/clip_by_global_norm
#https://github.com/tensorflow/tensorflow/blob/r1.8/tensorflow/python/ops/clip_ops.py

os.environ['CUDA_VISIBLE_DEVICES'] = ''

A = np.array([[1,1,2,4], [3,4,8,5]])
B = [1.,2.,3.,4.,5.]
print 'A:\n', A
print 'B:\n', B

# clip_by_global_norm test
clip_norm = 5
global_norm = np.sqrt(sum([(t)**2 for t in B]))
print global_norm
gg = [i * clip_norm / max(global_norm, clip_norm) for i in B]
print gg
with tf.Session() as sess:
	print sess.run(tf.clip_by_value(A,2,6))
	g_, norm_ = sess.run(tf.clip_by_global_norm(B, clip_norm))
	print g_
	print norm_
