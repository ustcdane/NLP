import numpy as np
from scipy.optimize import minimize
from scipy.stats import bernoulli, binom
np.random.seed(1234)
np.set_printoptions(formatter={'all':lambda x: '%.3f' % x})

# https://people.duke.edu/~ccc14/sta-663/EMAlgorithm.html

##################### complete information #######################################
#  https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.binom.html
def neg_loglik(thetas, n, xs, zs):
    return -np.sum([binom(n, thetas[z]).logpmf(x) for (x, z) in zip(xs, zs)])

m = 10
theta_A = 0.8
theta_B = 0.3
theta_0 = [theta_A, theta_B]

#  https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.bernoulli.html
coin_A = bernoulli(theta_A)
coin_B = bernoulli(theta_B)

# A,A,B,A,B.
xs = map(sum, [coin_A.rvs(m), coin_A.rvs(m), coin_B.rvs(m), coin_A.rvs(m), coin_B.rvs(m)])
zs = [0, 0, 1, 0, 1]


xs = np.array(xs)
print 'xs=',xs
ml_A = np.sum(xs[[0,1,3]])/(3.0*m)
ml_B = np.sum(xs[[2,4]])/(2.0*m)
print 'ml_A,ml_B:',ml_A, ml_B

bnds = [(0,1), (0,1)]
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
res = minimize(neg_loglik, [0.5, 0.5], args=(m, xs, zs),
         bounds=bnds, method='tnc', options={'maxiter': 100})

print res

######################## Incomplete information EM ############################

'''
i indicates the sample
j indicates the coin
l is an index running through each of the coins
alpha is the probability of the coin being heads
fa is the probability of choosing a particular coin
h is the number of heads in a sample
n is the number of coin tosses in a sample
k is the number of coins
m is the number of samples
'''

xs = np.array([(5,5), (9,1), (8,2), (4,6), (7,3)])
thetas = np.array([[0.6, 0.4], [0.5, 0.5]])

tol = 0.01
max_iter = 100

ll_old = 0
for i in range(max_iter):
    ws_A = []
    ws_B = []

    vs_A = []
    vs_B = []

    ll_new = 0

    # E-step: calculate probability distributions over possible completions
    for x in xs:

        # multinomial (binomial) log likelihood
        ll_A = np.sum([x*np.log(thetas[0])])
        ll_B = np.sum([x*np.log(thetas[1])])

        # [EQN 1]
        denom = np.exp(ll_A) + np.exp(ll_B)
        w_A = np.exp(ll_A)/denom
        w_B = np.exp(ll_B)/denom

        ws_A.append(w_A)
        ws_B.append(w_B)

        # used for calculating theta
        vs_A.append(np.dot(w_A, x))
        vs_B.append(np.dot(w_B, x))

        # update complete log likelihood
        ll_new += w_A * ll_A + w_B * ll_B

    # M-step: update values for parameters given current distribution
    # [EQN 2]
    thetas[0] = np.sum(vs_A, 0)/np.sum(vs_A)
    thetas[1] = np.sum(vs_B, 0)/np.sum(vs_B)
    # print distribution of z for each x and current parameter estimate

    print "Iteration: %d" % (i+1)
    print "theta_A = %.2f, theta_B = %.2f, ll = %.2f" % (thetas[0,0], thetas[1,0], ll_new)

    if np.abs(ll_new - ll_old) < tol:
        break
    ll_old = ll_new