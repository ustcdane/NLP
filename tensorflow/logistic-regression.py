# create a synthetic dataset for logistic regression
import numpy as np
import matplotlib.pyplot as plt

num_points = 100
vectors_set = []

for idx in range(num_points):
  x1 = np.random.normal(0.0, 1)
  y1 = 1 if x1 * 0.3 + 0.1 + np.random.normal(0.0, 0.03) > 0 else 0
  vectors_set.append([x1, y1])

x_data = [v[0] for v in vectors_set]
y_data = [v[1] for v in vectors_set]

#plot data
plt.plot(x_data, y_data, 'ro', label="Original data")
plt.legend()
plt.show()

# optimize linear regression with tensorflow
import tensorflow as tf

W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))

y = tf.sigmoid(W * x_data + b)
print('y.get_shape()',  y.get_shape())

# print(y.get_shape()[0])
one = tf.ones(y.get_shape(), dtype=tf.float32)
print(one.get_shape())

loss = -tf.reduce_mean(y_data * tf.log(y) + (one-y_data) * tf.log(one-y))

optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

# print sess.run(one)

print 'params-before-training\nW:', sess.run(W)
print 'b:', sess.run(b)

thresholdvec = tf.ones_like(one, dtype=tf.float32) * 0.5
#print sess.run(thresholdvec)

correct_prediction = tf.equal(tf.cast(y_data, tf.int32), tf.cast(tf.greater(y, thresholdvec), tf.int32))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

for step in xrange(201):
  sess.run(train)
  # print 'loss', (step, sess.run(loss))


  # print y_data.shape
  # print y.get_shape()

  # correct_prediction = tf.equal(tf.cast(y_data, tf.int32), tf.cast(tf.greater(y, thresholdvec), tf.int32))
  # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  # print type(y_data)
  if step % 20 == 0:
    print 'step:', step
    print('accuracy: ', sess.run(accuracy))
    print 'W:', sess.run(W)
    print 'b:', sess.run(b)
  # for idx in xrange(0, len(y_data)):
  #   print(y_data[idx], sess.run(y)[idx])

  # labelstr = "training step = " + (`step+1`)
  # plt.plot(x_data, y_data, 'ro', label=labelstr)
  # plt.plot(x_data, sess.run(W) * x_data + sess.run(b))
  # plt.legend()
  # plt.show()