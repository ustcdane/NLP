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
    global W,b # global �������޸� ��Ҫ�ڴ�����
    print  (np.dot(x,W)+b)*y
    if (np.dot(x,W)+b)*y<=0:# ������
        W+=np.array([(y*x)]).T#ע����ת�� ѧϰ��Ϊ1
        b+=y
        return W,b
    return W,b

#ʵ�ʵ�ѵ��
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


