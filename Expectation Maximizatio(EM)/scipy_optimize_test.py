#coding:utf-8

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import minimize,fmin_bfgs
import matplotlib.pyplot as pl


############### use  leastsq() to fit sin fun ##############################
# 数据拟合所用的函数: A*sin(2*pi*k*x + theta)
def func(x, p):
    A, k, theta = p
    return A * np.sin(2 * np.pi * k * x + theta)

# 实验数据x, y和拟合函数之间的差
def residuals(p, y, x):
    return y - func(x, p)


x = np.linspace(-2*np.pi, 0, 100)
A, k, theta = 10, 0.34, np.pi/6 # 真实数据的函数参数
y0 = func(x, [A, k, theta]) # 真实数据
y1 = y0 + 2 * np.random.randn(len(x)) # 加入噪声之后的实验数据

p0 = [7, 0.2, 0] # 第一次猜测的函数拟合参数
plsq = leastsq(residuals, p0, args=(y1, x)) # args参数，用于指定residuals中使用到的其他参数
# residuals()有三个参数，p是正弦函数的参数，y和x是表示实验数据的数组

print 'real parameter:', [A, k, theta] # 真实参数
print 'fitting parameter', plsq[0] # 实验数据拟合后的参数

pl.subplot(211)
pl.plot(x, y0, label="real data")
pl.plot(x, y1, label="Experimental data with noise")
pl.plot(x, func(x, plsq[0]), label="fitting data")
pl.legend()
#pl.show()

############### use  minimize() to fit sin fun ##############################
# http://blog.chinaunix.net/uid-21633169-id-4437868.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
# minimize(fun, x0[, args, method, jac, hess, ...])Minimization of scalar function of one or more variables.

def fun(x):
    return x**2 +  10* np.sin(x)
x = np.arange(-10, 10, 0.1)
pl.subplot(212)
pl.plot(x, fun(x))


res = fmin_bfgs(fun, 0)
print 'when init is 0:',res

res = fmin_bfgs(fun, 3, disp=0)
print 'when init is 3:',res

res = minimize(fun, 0, method='L-BFGS-B')
print 'use minimize:',res
pl.show()