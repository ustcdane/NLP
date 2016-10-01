import numpy as np

X=np.array([[3,3],[4,3],[1,1]])
print 'X:\n',X

Y=np.array([[1,1,-1]])
Y=Y.T
print 'y:\n',Y

W=np.array([[0,0]]).T
b=0
print 'w:\n',W


def train(x,y):
    global W,b # global 变量有修改 需要在此申明
    print  (np.dot(x,W)+b)*y
    if (np.dot(x,W)+b)*y<=0:# 误分类点
        W+=np.array([(y*x)]).T#注意结果转置 学习率为1
        b+=y
        return W,b
    return W,b

#实际的训练
cnt=0
while True:
    for i,x in enumerate(X):
        W1,b1 = W.copy(), b
        print 'x:',x
        print 'y:',Y[i]
        train(x,Y[i])
        if (W1==W).all() and b==b1:#
            cnt+=1
    if cnt==3:
        break
    cnt=0
print 'result'
print W
print b


