# The purpose of this exercise is for you to understand better the
# backpropagation algorithm and stochastic gradient descent
# algorithm. In the following, I will create a dataset similar to the
# one in the tutorials and a neural network of one hidden
# layer. Search for WORK to find the places that you're supposed to
# fill in the necessary code.

from random import random, randint
from math import exp
from copy import deepcopy

# Find the size of matrix M
def size_matrix(M):
  return [len(M), len(M[0])]

# Find the size of vector v
def size_vector(v):
  return [len(v)]

# Multiply matrix M with vector v
def dot(M, v):
  u = [];
  for i in xrange(len(M)):
    val = 0.0
    for j in xrange(len(M[i])):
      val = val + M[i][j] * v[j]
    u.append(val)
  return u

# Cross product between u and v (u*v')
def cross(u, v):
  M = []
  for i in xrange(len(u)):
    N = []
    for j in xrange(len(v)):
      N.append(u[i] * v[j])
    M.append(N)
  return M

# Compute the elementwise dot-product of u and v
def ew_dot(u,v):
  w = [];
  for i in xrange(len(u)):
    w.append(u[i] * v[i])
  return w

# Compute the addition of u and v
def add(u,v):
  w = [];
  for i in xrange(len(u)):
    w.append(u[i] + v[i])
  return w

# Compute the addition of u and v
def add_matrix(U,V):
  W = [];
  for i in xrange(len(U)):
    temp = []
    for j in xrange(len(U[i])):
      temp.append(U[i][j] + V[i][j])
    W.append(temp)
  return W

# Compute the sigmoid function on every dimension of the vector v and
# the derivative.
def sigmoid(v):
  u = []
  w = []
  for i in xrange(len(v)):
    a = 1. / (1 + exp(-v[i]))
    u.append(a)
    w.append(a*(1-a))
  return [u,w]

# Multiply the scale a with vector v
def scale(a, v):
  u = []
  for i in xrange(len(v)):
    u.append(a * v[i])
  return u

# Multiply the scale a with vector v
def scale_matrix(a, M):
  N = []
  for i in xrange(len(M)):
    U = []
    for j in xrange(len(M[i])):
      U.append(a * M[i][j])
    N.append(U)
  return N

# Transpose a matrix M
def transpose(M):
  N = []
  for j in xrange(len(M[0])):
    U = []
    for i in xrange(len(M)):
      U.append(M[i][j])
    N.append(U)
  return N

# Forward pass to compute the activation at every layer
def forprop(Yi, Xi, W1, b1, W2, b2):
  h1 = Xi;
  temp = dot(W1, Xi)
  temp = add(temp, b1)
  [h2, dh2] = sigmoid(temp) # activation at layer 1, and its derivative
  temp = dot(W2, h2)
  temp = add(temp, b2)
  [h3, dh3] = sigmoid(temp) # activation at layer 2, and its derivative

  # Compute the objective function
  diff = (h3[0] - Yi)
  J = diff * diff;

  return [J, diff, h1, h2, dh2, h3, dh3]

# Backward pass to compute the gradient for every parameter
def backprop(Yi, Xi, W1, b1, W2, b2):
  # forward pass to compute the activation at each layer
  [J, diff, h1, h2, dh2, h3, dh3] = forprop(Yi, Xi, W1, b1, W2, b2)
  ###########################################
  # WORK: Fill in your gradient computation here
  ###########################################
  # Right now i am just setting the gradient the same as the
  # parameters. Replace the following 4 lines with your own backprop
  # computation (could be longer than 4 lines).
  W2grad = W2;
  W1grad = W1;
  b2grad = b2;
  b1grad = b1;
  return [J, W1grad, b1grad, W2grad, b2grad]

# Check the gradient computation from backprop
def checkgrad(Yi, Xi, W1, b1, W2, b2):
  [J, W1grad, b1grad, W2grad, b2grad] = backprop(Yi, Xi, W1, b1, W2, b2)

  epsilon = 0.001
  tolerance = epsilon

  # check the gradient for W2
  for i in xrange(len(W2)):
    for j in xrange(len(W2[i])):
      W2new = deepcopy(W2)
      W2new[i][j] = W2new[i][j] + epsilon
      [Jnew, diff, h1, h2, dh2, h3, dh3] = forprop(Yi, Xi, W1, b1, W2new, b2)
      numgrad = (Jnew - J) / epsilon
      if abs(numgrad - W2grad[i][j]) > tolerance:
        s = "numerical gradient of W2 at "
        s = s + str(i) + "," + str(j)
        s = s + " do not match with analytical gradient: "
        s = s + str(numgrad) + " vs. " + str(W2grad[i][j])
        print s
        return False

  # check the gradient for b2
  for i in xrange(len(b2)):
    b2new = deepcopy(b2)
    b2new[i] = b2new[i] + epsilon
    [Jnew, diff, h1, h2, dh2, h3, dh3] = forprop(Yi, Xi, W1, b1, W2, b2new)
    numgrad = (Jnew - J) / epsilon
    if abs(numgrad - b2grad[i]) > tolerance:
      s = "numerical gradient of b2 at "
      s = s + str(i) + "," + str(j)
      s = s + " do not match with analytical gradient: "
      s = s + str(numgrad) + " vs. " + str(b2grad[i])
      print s
      return False

  # check the gradient for W1
  for i in xrange(len(W1)):
    for j in xrange(len(W1[i])):
      W1new = deepcopy(W1)
      W1new[i][j] = W1new[i][j] + epsilon
      [Jnew, diff, h1, h2, dh2, h3, dh3] = forprop(Yi, Xi, W1new, b1, W2, b2)
      numgrad = (Jnew - J) / epsilon
      if abs(numgrad - W1grad[i][j]) > tolerance:
        s = "numerical gradient of W1 at "
        s = s + str(i) + "," + str(j)
        s = s + " do not match with analytical gradient: "
        s = s + str(numgrad) + " vs. " + str(W1grad[i][j])
        print s
        return False

  # check the gradient for b1
  for i in xrange(len(b1)):
    b1new = deepcopy(b1)
    b1new[i] = b1new[i] + epsilon
    [Jnew, diff, h1, h2, dh2, h3, dh3] = forprop(Yi, Xi, W1, b1new, W2, b2)
    numgrad = (Jnew - J) / epsilon
    if abs(numgrad - b1grad[i]) > tolerance:
      s = "numerical gradient of b1 at "
      s = s + str(i) + "," + str(j)
      s = s + " do not match with analytical gradient: "
      s = s + str(numgrad) + " vs. " + str(b1grad[i])
      print s
      return False

  return True

# Classify example Xi, using parameters W1, b1, W2, b2
# if raw_prediction is True, return the decision function 
# value without mapping to 0 or 1.
def classify(Xi, W1, b1, W2, b2, raw_prediction=False):
  h1 = Xi;
  temp = dot(W1, Xi)
  temp = add(temp, b1)
  [h2, dh2] = sigmoid(temp) # activation at layer 1, and its derivative
  temp = dot(W2, h2)
  temp = add(temp, b2)
  [h3, dh3] = sigmoid(temp) # activation at layer 2, and its derivative
  
  if raw_prediction:
    return h3[0]
  
  # Check if we make an error
  if h3[0] > 0.5:
    return 1
  else:
    return 0

# stochastic gradient descent on dataset X, Y, with learning rate alpha
def sgd(X, Y, alpha):
  W1 = [[random(), random()],
        [random(), random()],
      [random(), random()]]
  b1 = [0, 0, 0];
  W2 = [[random(), random(), random()]]
  b2 = [0];

  # Checking the gradient computed by backprop
  if checkgrad(Y[0], X[0], W1, b1, W2, b2):
    print "Gradient check passed."
  else:
    print "Gradient check failed."

  # Iterate 10000 times, each time with one example randomly sampled
  # from the dataset
  for i in xrange(10000):
    # Sample one example from the dataset
    index = randint(0,len(X)-1) # this is the index of the example

    # Run backprop to compute the gradient
    [J, W1grad, b1grad, W2grad, b2grad] = backprop(Y[index], X[index], W1, b1, W2, b2)
    # Use the computed gradient to update parameters
    ###########################################
    # WORK: Fill in your stochastic updates here
    ###########################################
    # For now, I just keep the parameters to be the same. Replace the
    # following 4 lines with your own updates.
    W1 = W1;
    W2 = W2;
    b1 = b1;
    b2 = b2;

  # Bookkeeping, compute the objective function and how many
  # misclassified examples
  J = 0 # overall objective function
  E = 0 # number of misclassified examples
  for index in xrange(len(X)):
    # Compute the objective function at the example
    [J_index, W1grad, b1grad, W2grad, b2grad] = backprop(Y[index], X[index], W1, b1, W2, b2)
    J = J + J_index
    # classify the example and compare with the ground truth
    prediction = classify(X[index], W1, b1, W2, b2)
    if prediction != Y[index]:
      E = E + 1
  print "Learning rate: " + str(alpha) + ", objective: " + str(J) + ", number of errors: " + str(E)

  # This is the optimal parameters
  return [W1, b1, W2, b2]

# Visualize data and decision function using pylab
def display_decision_function(X, Y, W1, b1, W2, b2):
  import pylab
  xpoints_neg = []
  ypoints_neg = []
  xpoints_pos = []
  ypoints_pos = []
  for i in xrange(len(X)):
    if Y[i] < 0.5:
      xpoints_neg.append(X[i][0])
      ypoints_neg.append(X[i][1])
    else:
      xpoints_pos.append(X[i][0])
      ypoints_pos.append(X[i][1])

  pylab.plot(xpoints_neg, ypoints_neg, 'bx',markersize=10)
  pylab.plot(xpoints_pos, ypoints_pos, 'ro',markersize=10)

  pylab.plot(3,3, 'md',markersize=10)

  decision_boundary = []
  xpoints = []
  ypoints = []
  steps = [x * 0.1 for x in range(0, 60)]
  for xpoint in steps:
    for ypoint in steps:
      prediction = classify([xpoint,ypoint], W1, b1, W2, b2, True)
      if abs(prediction - 0.5) < 0.03:
        decision_boundary.append([xpoint, ypoint])
        xpoints.append(xpoint)
        ypoints.append(ypoint)
  pylab.plot(xpoints, ypoints, 'g.')
  pylab.xlabel('Mary rating')
  pylab.ylabel('John rating')
  pylab.xlim([0,6])
  pylab.ylim([0,6])
  pylab.grid(True)
  pylab.legend(['Movies that I dislike', 'Movies that I like', 'Gravity', 'Decision function'],loc=4);
  pylab.show()

# main function
if __name__ == "__main__":
  # dataset, each example is a pair of ratings
  X = [[1,5],[2.5,5],[3.5,5],[4.5,5], [1, 4], [1.5, 4], [3.5,4], [4.5, 4], [2.5, 3], [2.5, 1.5], [2.5, 1]]
  # each label has a value of either 0 or 1 indicating if I will like
  # the movie or not
  Y = [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0]

  # running sgd with the learning rate alpha = 1
  [W1, b1, W2, b2] = sgd(X, Y, 1)
  prediction = classify([3,3], W1, b1, W2, b2)

  if prediction == 0:
    print "Rating (3,3), I will not like this movie"
  else:
    print "Rating (3,3), I will like this movie"

  visualize = True # set this variable to True to visualize the data
  if visualize == True:
    print
    print "For visualization, you need pylab"
    display_decision_function(X, Y, W1, b1, W2, b2)
