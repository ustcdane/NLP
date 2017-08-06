
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
</br></br>这样， 我 们 得 到 了 一 个 基 于 文 档 集 合D = {d1, d2, ..., dN}和 词 表W ={w1, w2, ..., wM}上的观察矩阵N = (n(di, wj))ij。对于每一观察数据< di, wj >我们假设中间关联一个隐含的主题变量zk ∈ {z1, z2, ..., zK}。我们可以认为主题类别zk是文档中所涉及的概念或者主题。每个文档中可以讨论多个概念或者主题。因此原来的观测二元组< di, wj >就被扩展成了三元组< di, zk, wj >，其中zk是非观测值。在观测矩阵N = (n(di, wj))ij上，我们用如下的框架定义生成模型：

* 以概率P r(di)选择一个文档di；
* 以概率Pr(zk|di)挑选一个隐性的主题类别zk。
* 以概率Pr(wj|zk)生成一个词wj；
</br>
用贝叶斯网络的语言描述这个过程如下图所示: </br>
![plsa-bayesian](https://github.com/ustcdane/NLP/blob/master/PLSA/img/plsa-bayesian.png)

</br>

基于上图，我们可以把观测数据<di, wj >的联合概率Pr(di, wj)写成在主题上的边缘概率的和$\sum_{m=0}^\inft P Pr(di, zk, wj)，然后基
于贝叶斯网络进行分解得到Pr(di, wj) =KX k=1Pr(di)Pr(zk|di)Pr(wj|zk)







## 3. PLSA 求解

PLSA通过[EM](https://github.com/ustcdane/NLP/tree/master/Expectation%20Maximizatio(EM))算法，极大化关于隐变量主题Z_k的后验概率似然的期望（极大化过程是带两个约束条件的，所以用拉格朗日乘法来求解），利用EM算法进行反复的迭代计算直至收敛。




# ref 
from  [PLSA](http://zhikaizhang.cn/2016/06/17/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86%E4%B9%8BPLSA/)