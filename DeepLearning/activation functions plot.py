#!/bin/env python
#coding:utf-8
#By Danile Wang 2016-04-12
'''
非线性 可微 单调
'''
#http://blog.csdn.net/cyh_24/article/details/50593400

import matplotlib.pyplot as plt
import numpy as np

# x axis data
x=np.arange(-3,3,0.1)
#rectifier_x=np.arange(-1.1,1.1,0.1)
#y axis data
sigmoid_y=[np.exp(i)/(1+np.exp(i)) for i in x]
tanh_y=[np.tanh(i) for i in x]
rectifier_y=[max(0,i) for i in x]
softplus_y=[np.log(1+np.exp(i)) for i in x]

plt.plot(x, tanh_y, '-', label=u'tanh')
plt.plot(x,sigmoid_y,'-', label=u'sigmoid')
plt.plot(x,rectifier_y,'-', label=u'rectfier')
plt.plot(x,softplus_y,'-', label=u'softplus')

plt.legend(loc='upper left')#显示标签，或者说图例
plt.grid(True)
plt.show()
