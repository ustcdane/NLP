
# PLSA (Probabilistic Latent Semantic Analysis) 

This is a python implementation of Probabilistic Latent Semantic Analysis using EM algorithm.

Support both English and Chinese.

# Usage

Execute the following command in the cmd :

```
python plsa.py [datasetFilePath] [stopwordsFilePath] [K] [maxIteration] [threshold] [topicWordsNum] [docTopicDisFilePath] [topicWordDisFilePath] [dictionaryFilePath] [topicsFilePath]
```

eg. 

```
python plsa.py dataset.txt stopwords.dic 10 30 1.0 10 doctopic.txt topicword.txt dictionary.dic topics.txt 
```

or omit the params using default values specified in plsa.py :

```
python plsa.py
```

The meaning of params are given as following:

|param|description|
|:---:|:---------:|
|datasetFilePath|the file path of dataset|
|stopwordsFilePath|the file path of stopwords|
|K|the number of topic|
|maxIteration|the max number of iteration of EM algorithm|
|threshold|the threshold to judge the convergence of log likelihood|
|topicWordsNum|the number of top words of each topic|
|docTopicDisFilePath|the file path to output document-topic distribution|
|topicWordDistribution|the file path to output topic-word distribution|
|dictionaryFilePath|the file path to output dictionary|
|topicsFilePath|the file path to output top words of each topic|

# Format of inputs

In the dataset file, each line represents a document.

In the stopwords file, each line represents a stopword.

# Samples

## Dataset 1(English)

The first dataset is 16 documents about one piece from wikipedia.

The params are set as :

```
python plsa.py dataset1.txt stopwords.dic 10 20 1.0 10 doctopic.txt topicword.txt dictionary.dic topics.txt 
```

## Dataset 2(English)

The second dataset is 100 documents from the Associated Press.

The params are set as :

```
python plsa.py dataset2.txt stopwords.dic 10 20 50.0 10 doctopic.txt topicword.txt dictionary.dic topics.txt 
```

## Dataset 3(Chinese)

The third dataset is 50 documents from sina.

The params are set as :

```
python plsa.py dataset3.txt stopwords.dic 30 30 10.0 10 doctopic.txt topicword.txt dictionary.dic topics.txt 
```


# note (Chinese)

## 1. PLSA

PLSA(Probabilistic Latent Semantic Analysis, 概率潜在语义分析)由LSA发展而来。LSA使用线性代数方法，对document-word矩阵进行SVD分解。PLSA则使用了一个概率图模型，引入了一个隐变量topic（可以认为是文档的主题），然后进行统计推断。
在语义分析问题中，存在同义词和一词多义这两个严峻的问题，LSA可以很好的解决同义词问题，却无法妥善处理一词多义问题。PLSA则可以同时解决同义词和一词多义两个问题。

## 2. PLSA 原理

我们知道文档(一个句子、一个段落或一篇文章)都有它自己的主题，从大的方面讲有经济、历史、音乐、运动、游戏、法律等等主题，PLSA模型就引入了一个隐变量topic来表示这个主题。
假如给定一个文档集合记为D = {d1, d2, ..., dN}，每个文档中由若干词组成。通过统计得到所有文档中的词表为W = {w1, w2, ..., wM}。如果忽略文档中词的序列，我们可以把观察数据记为一个“文档-词”矩阵，如下图所示。</br>
![doc-word](https://github.com/ustcdane/NLP/blob/master/PLSA/img/doc-word.png)
</br></br>这样， 我 们 得 到 了 一 个 基 于 文 档 集 合D = {d1, d2, ..., dN}和 词 表W ={w1, w2, ..., wM}上的观察矩阵N = (n(di, wj))ij。对于每一观察数据< di, wj >我们假设中间关联一个隐含的主题变量zk ∈ {z1, z2, ..., zK}。我们可以认为主题类别zk是文档中所涉及的概念或者主题。每个文档中可以讨论多个概念或者主题。因此原来的观测二元组< di, wj >就被扩展成了三元组< di, zk, wj >，其中zk是非观测值，是隐藏变量。在观测矩阵N = (n(di, wj))ij上，我们用如下的框架定义生成模型：

* 以概率p(di)选择一个文档di；
* 以概率p(zk|di)挑选一个隐性的主题类别zk。
* 以概率p(wj|zk)生成一个词wj；
</br>
用贝叶斯网络的语言描述这个过程如下图所示: </br>

![plsa-bayesian](https://github.com/ustcdane/NLP/blob/master/PLSA/img/plsa-bayesian.png)

</br>
基于上图，我们可以把观测数据<di, wj >的联合概率p(di, wj)写成在主题上的边缘概率的和SUM_k{p(di, zk, wj)},其中k=1,2...K，然后基
于贝叶斯网络进行分解得到p(di, wj) =SUM_k{p(di)p(zk|di)p(wj|zk)},k=1,2...K。</br>

![plsa-prob](https://github.com/ustcdane/NLP/blob/master/PLSA/img/plsa-joint.png)

</br>第一个等式是对三者的联合概率分布对其中的隐藏变量 Z 的所有取值累加，第二个等式根据图模型的依赖关系将联合概率展开为条件概率，第三个等式只是简单的乘法结合律。这样就计算出了第 i 篇文档与第 j 个单词的联合概率分布。

**complete-data log likelihood** </br>
我们可以得到完整数据的对数似然为：

![cp-data](https://github.com/ustcdane/NLP/blob/master/PLSA/img/complete-data.png)

其中 n(di,wj) 表示第 j 个word在第 i 个document中出现的次数。
上式左边一项对于给定的数据集来说是定值，我们只需要使得右边一项取到最大。
p(zk|di)和p(wj|zk) 是PLSA模型需要求解的参数,**注意**这里的参数以求和的形式出现在了对数函数之中，求导结果十分复杂，无法使用取偏导数并令偏导为0的方法。
因为，含有隐变量，因此使用[EM](https://github.com/ustcdane/NLP/tree/master/Expectation%20Maximizatio(EM))算法。


## 3. PLSA 求解

PLSA通过[EM](https://github.com/ustcdane/NLP/tree/master/Expectation%20Maximizatio(EM))算法，极大化关于隐变量主题Z_k的后验概率似然的期望（极大化过程是带两个约束条件的，所以用拉格朗日乘法来求解），利用EM算法进行反复的迭代计算直至收敛。
对于求解PLSA相关参数的EM算法的步骤是: </br>
1. E-step: 我们假定待估参数 p(zk|di)和p(wj|zk)是给定的，计算隐变量zk的后验条件概率分布p(zk|di,wj)
2. M-step: 假定隐变量已经确定的条件下，即在E-step后我们可以认为此事的数据是完全的。最大化最大似然函数的期望（即Q函数）。此时我们使用E-step里计算的隐变量的后验概率p(zk|di,wj)
，得到新的估计参数值p(zk|di)和p(wj|zk)。

</br>
![EM1](https://github.com/ustcdane/NLP/blob/master/PLSA/img/EM1.png)
</br>
![EM2](https://github.com/ustcdane/NLP/blob/master/PLSA/img/EM2.png)
</br>

那么何时停止EM算法呢？一种方法是计算完整数据的对数似然，当这个值的变化小于某个阈值时认为已经收敛；另一种方法可以固定迭代次数，进行截断，避免过拟合。
这就是最大似然估计来确定PLSA待估参数p(zk|di)和p(wj|zk)的过程。如果我们对隐变量zk没有先验知识，那么最大似然估计是合理的。如果我们对文档产生主题p(zk|di)和主题产生词p(wj|zk)的分布
有先验知识，那么我们就应该用贝叶斯估计，这就是LDA要解决的问题，本质上PLSA和非负矩阵分解(NMF)是等价的。


# ref 
from  [PLSA](http://zhikaizhang.cn/2016/06/17/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86%E4%B9%8BPLSA/)