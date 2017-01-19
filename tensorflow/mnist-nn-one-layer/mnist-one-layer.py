import tensorflow as tf

import input_mnist
mnist = input_mnist.read_data_sets("mnist-data/", one_hot=True)

print mnist.train.images.shape
print mnist.train.labels.shape
print mnist.test.images.shape
print mnist.test.labels.shape

# print mnist.IMAGE_PIXELS

W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

x = tf.placeholder("float", [None, 784])

y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder("float", [None, 10])

#print type(x),x,'type y:\n', type(y)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

for i in xrange(101):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    _, loss_value, y_pred = sess.run([train_step, cross_entropy, y], feed_dict={x: batch_xs, y_: batch_ys})
    if i % 10 ==0:
        print '--' * 20
        print 'step %d:' % i
        print 'In minibatch the last instance:'
        print 'prob:'
        print y_pred[-1]
        print 'real label:'
        print batch_ys[-1]
        print '\ncross_entropy:%.2f' % (loss_value)
print "\nresult:"
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print 'Accuracy: %.4f' % (sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
