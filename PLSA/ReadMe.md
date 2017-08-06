
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

PLSA(Probabilistic Latent Semantic Analysis, ����Ǳ���������)��LSA��չ������LSAʹ�����Դ�����������document-word�������SVD�ֽ⡣PLSA��ʹ����һ������ͼģ�ͣ�������һ��������topic��������Ϊ���ĵ������⣩��Ȼ�����ͳ���ƶϡ�
��������������У�����ͬ��ʺ�һ�ʶ����������Ͼ������⣬LSA���ԺܺõĽ��ͬ������⣬ȴ�޷����ƴ���һ�ʶ������⡣PLSA�����ͬʱ���ͬ��ʺ�һ�ʶ����������⡣

## 2. PLSA ԭ��

����֪���ĵ�(һ�����ӡ�һ�������һƪ����)�������Լ������⣬�Ӵ�ķ��潲�о��á���ʷ�����֡��˶�����Ϸ�����ɵȵ����⣬PLSAģ�;�������һ��������topic����ʾ������⡣
�������һ���ĵ����ϼ�ΪD = {d1, d2, ..., dN}��ÿ���ĵ��������ɴ���ɡ�ͨ��ͳ�Ƶõ������ĵ��еĴʱ�ΪW = {w1, w2, ..., wM}����������ĵ��дʵ����У����ǿ��԰ѹ۲����ݼ�Ϊһ�����ĵ�-�ʡ���������ͼ��ʾ��</br>
![doc-word](https://github.com/ustcdane/NLP/blob/master/PLSA/img/doc-word.png)
</br></br>������ �� �� �� �� �� һ �� �� �� �� �� �� ��D = {d1, d2, ..., dN}�� �� ��W ={w1, w2, ..., wM}�ϵĹ۲����N = (n(di, wj))ij������ÿһ�۲�����< di, wj >���Ǽ����м����һ���������������zk �� {z1, z2, ..., zK}�����ǿ�����Ϊ�������zk���ĵ������漰�ĸ���������⡣ÿ���ĵ��п������۶������������⡣���ԭ���Ĺ۲��Ԫ��< di, wj >�ͱ���չ������Ԫ��< di, zk, wj >������zk�Ƿǹ۲�ֵ�������ر������ڹ۲����N = (n(di, wj))ij�ϣ����������µĿ�ܶ�������ģ�ͣ�

* �Ը���p(di)ѡ��һ���ĵ�di��
* �Ը���p(zk|di)��ѡһ�����Ե��������zk��
* �Ը���p(wj|zk)����һ����wj��
</br>
�ñ�Ҷ˹������������������������ͼ��ʾ: </br>

![plsa-bayesian](https://github.com/ustcdane/NLP/blob/master/PLSA/img/plsa-bayesian.png)

</br>
������ͼ�����ǿ��԰ѹ۲�����<di, wj >�����ϸ���p(di, wj)д���������ϵı�Ե���ʵĺ�SUM_k{p(di, zk, wj)},����k=1,2...K��Ȼ���
�ڱ�Ҷ˹������зֽ�õ�p(di, wj) =SUM_k{p(di)p(zk|di)p(wj|zk)},k=1,2...K��</br>

![plsa-prob](https://github.com/ustcdane/NLP/blob/master/PLSA/img/plsa-joint.png)

</br>��һ����ʽ�Ƕ����ߵ����ϸ��ʷֲ������е����ر��� Z ������ȡֵ�ۼӣ��ڶ�����ʽ����ͼģ�͵�������ϵ�����ϸ���չ��Ϊ�������ʣ���������ʽֻ�Ǽ򵥵ĳ˷�����ɡ������ͼ�����˵� i ƪ�ĵ���� j �����ʵ����ϸ��ʷֲ���

** complete-data log likelihood **
���ǿ��Եõ��������ݵĶ�����ȻΪ��

![plsa-bayesian](https://github.com/ustcdane/NLP/blob/master/PLSA/img/complete-data.png)

���� n(di,wj) ��ʾ�� j ��word�ڵ� i ��document�г��ֵĴ�����
��ʽ���һ����ڸ��������ݼ���˵�Ƕ�ֵ������ֻ��Ҫʹ���ұ�һ��ȡ�����
p(zk|di)��p(wj|zk) ��PLSAģ����Ҫ���Ĳ���,**ע��**����Ĳ�������͵���ʽ�������˶�������֮�У��󵼽��ʮ�ָ��ӣ��޷�ʹ��ȡƫ��������ƫ��Ϊ0�ķ�����
��Ϊ�����������������ʹ��[EM](https://github.com/ustcdane/NLP/tree/master/Expectation%20Maximizatio(EM))�㷨��


## 3. PLSA ���

PLSAͨ��[EM](https://github.com/ustcdane/NLP/tree/master/Expectation%20Maximizatio(EM))�㷨�����󻯹�������������Z_k�ĺ��������Ȼ�����������󻯹����Ǵ�����Լ�������ģ��������������ճ˷�����⣩������EM�㷨���з����ĵ�������ֱ��������




# ref 
from  [PLSA](http://zhikaizhang.cn/2016/06/17/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86%E4%B9%8BPLSA/)