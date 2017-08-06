#!/bin/bash


# for Chinese test
echo 'For Chinese test'
python plsa.py dataset3.txt stopwords.dic 30 30 10.0 10 doctopic.txt topicword.txt dictionary.dic topics.txt 
