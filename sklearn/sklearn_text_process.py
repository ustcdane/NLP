#http://blog.csdn.net/abcjennifer/article/details/23615947/
#first extract the 20 news_group dataset to /scikit_learn_data
from sklearn.datasets import fetch_20newsgroups
from pprint import pprint
#all categories
#newsgroup_train = fetch_20newsgroups(subset='train')
#part categories
categories = ['comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x'];
newsgroup_train = fetch_20newsgroups(subset = 'train',categories = categories)
newsgroup_test = fetch_20newsgroups(subset = 'test',categories = categories)
print 'Train Data:\n'
pprint(list(newsgroup_train.target_names))
print 'Test Data:\n'
pprint(list(newsgroup_test.target_names))
print type(newsgroup_train.data)
print type(newsgroup_train)
print '-'*20
#print newsgroup_train.data[0]
print '-'*20
#print newsgroup_train.data[1]
print '-|-'*20
newsgroup_test.data[0]
print '-'*20

#newsgroup_train.data is the original documents, but we need to extract the 
#feature vectors inorder to model the text data
from sklearn.feature_extraction.text import HashingVectorizer
vectorizer = HashingVectorizer(stop_words = 'english',non_negative = True,
                               n_features = 10000)
fea_train = vectorizer.fit_transform(newsgroup_train.data)
fea_test = vectorizer.fit_transform(newsgroup_test.data);

print '-'*20
print fea_train.shape[0], fea_train.shape[1],fea_train.nnz

print '-^-'*20
print type(fea_train)#,fea_train[1]
print '-'*20

print '-*-'*20
print type(fea_train[0])#,fea_train[2]
print '-'*20

print '-&-'*20
print type(newsgroup_train.target)
print newsgroup_train.target[:20]
print '-'*20

#return feature vector 'fea_train' [n_samples,n_features]
print 'Size of fea_train:' + repr(fea_train.shape)
print 'Size of fea_train:' + repr(fea_test.shape)
#11314 documents, 130107 vectors for all categories
print 'The average feature sparsity is {0:.3f}%'.format(
fea_train.nnz/float(fea_train.shape[0]*fea_train.shape[1])*100);


#----------------------------------------------------
#method 1:CountVectorizer+TfidfTransformer
print '*************************\nCountVectorizer+TfidfTransformer\n*************************'
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
count_v1= CountVectorizer(stop_words = 'english', max_df = 0.5);
counts_train = count_v1.fit_transform(newsgroup_train.data);
print "the shape of train is "+repr(counts_train.shape)

count_v2 = CountVectorizer(vocabulary=count_v1.vocabulary_);
counts_test = count_v2.fit_transform(newsgroup_test.data);
print "the shape of test is "+repr(counts_test.shape)

tfidftransformer = TfidfTransformer();

tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train);
tfidf_test = tfidftransformer.fit(counts_test).transform(counts_test);

######################################################
#Multinomial Naive Bayes Classifier
print '*************************\nNaive Bayes\n*************************'
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

def calculate_result(actual,pred):
    m_precision = metrics.precision_score(actual,pred);
    m_recall = metrics.recall_score(actual,pred);
    print 'predict info:'
    print 'precision:{0:.3f}'.format(m_precision)
    print 'recall:{0:0.3f}'.format(m_recall);
    print 'f1-score:{0:.3f}'.format(metrics.f1_score(actual,pred));
    


newsgroups_test = fetch_20newsgroups(subset = 'test',
                                     categories = categories);
fea_test = vectorizer.fit_transform(newsgroups_test.data);
#create the Multinomial Naive Bayesian Classifier
clf = MultinomialNB(alpha = 0.01) 
clf.fit(fea_train,newsgroup_train.target);
pred = clf.predict(fea_test);
calculate_result(newsgroups_test.target,pred);
#notice here we can see that f1_score is not equal to 2*precision*recall/(precision+recall)
#because the m_precision and m_recall we get is averaged, however, metrics.f1_score() calculates
#weithed average, i.e., takes into the number of each class into consideration.

######################################################
#SVM Classifier
from sklearn.svm import SVC
print '*************************\nSVM\n*************************'
svclf = SVC(kernel = 'linear')#default with 'rbf'
svclf.fit(fea_train,newsgroup_train.target)
pred = svclf.predict(fea_test);
calculate_result(newsgroups_test.target,pred);
