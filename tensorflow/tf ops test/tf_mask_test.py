# Lab 7 Learning rate and Evaluation
import tensorflow as tf
import random
tf.set_random_seed(777)  # for reproducibility
import numpy as np
import os
import pdb
os.environ['CUDA_VISIBLE_DEVICES'] = ''
#config = tf.ConfigProto()

one_hot = tf.one_hot(indices=[0,2,1,-1],depth=3,on_value=1,off_value=0,axis=-1)

## inputs tensor
x = tf.placeholder(tf.int32, [None, None], name='x')  # sentence
in_mask = tf.placeholder(tf.float32, [None, None], name='in_mask')  # mask
### look_up 
vocabulary_size=10
embedding_size = 2
w_embed = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0), name='w_embed')

# inputs em
embed = tf.nn.embedding_lookup(w_embed, x)
# get echo sentence's length
mask_sum = tf.reduce_sum(in_mask, 1)

# input xx real data
batch_size=4
sequence_length=5
xx=np.zeros((batch_size, sequence_length),dtype=np.int32)
xx[0][:1] = 1
xx[1][:3] = 2
xx[2][:2] = 3 
xx[3][:4] = 4 

sq_mask_float = tf.sequence_mask([1, 3, 2, 4], maxlen=5, dtype=tf.float32)
# [batch_size, sentence_len] --> [batch_size, sentence_len, embedding] to multiply inputs embedding
batch_seq_em_mask = tf.expand_dims(in_mask, 2)
#batch_seq_em_mask = in_mask[:,:,None]

# To ignore sentence's mask 0 word's embeding
mask_em = tf.multiply(embed, batch_seq_em_mask)
#mask_em = embed*batch_seq_em_mask

em_sum = tf.reduce_sum(mask_em, 1)
# get each sentence's mean embedding
#sen_vec = em_sum /((mask_sum)[:, None])
sen_vec = em_sum /tf.expand_dims(mask_sum,1)

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	one,mask = sess.run([one_hot, sq_mask_float])
	print 'one_hot:\n', one
	print 'input shape:\n', xx.shape
	print 'input xx:\n', xx
	print 'mask:\n',mask
	em, ms, es, sen= sess.run([embed, mask_sum, em_sum,sen_vec], feed_dict={x:xx, in_mask:mask})
	print 'type(em)', type(em)
	print 'input embedding shape:', em.shape
	print 'input embedding:\n', em
	
	print 'mask sum shape:', ms.shape
	print 'mask sum:\n', ms
	print '(mask_sum)[:, None]):\n', ms[:, None]
	
	print 'sen vec shape:', sen.shape
	print 'sen vec:\n', sen
	
	#print ' em_sum shape:', es.shape
	#print 'em_sum :\n', es
