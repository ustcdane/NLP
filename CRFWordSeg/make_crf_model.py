#coding:utf-8
import sys
import os
import argparse
from multiprocessing import cpu_count

# options of crf_leaern:
# -c float: 
# With this option, you can change the hyper-parameter for the CRFs.
# With larger C value, CRF tends to overfit to the give training corpus.
# This parameter trades the balance between overfitting and underfitting.
# The results will significantly be influenced by this parameter.
# You can find an optimal value by using held-out data or more general model selection method such as cross validation.

# -f NUM:
# This parameter sets the cut-off threshold for the features.
# CRF++ uses the features that occurs no less than NUM times in the given training data.
# The default value is 1.
# When you apply CRF++ to large data,
# the number of unique features would amount to several millions.
# This option is useful in such cases.

# -p NUM:
# If the PC has multiple CPUs,
# you can make the training faster by using multi-threading.
# NUM is the number of threads.

def crf_train_modle(template, input, model):
    cmd_learn = 'crf_learn -c 5 -p ' + str(cpu_count())
    cmd_learn += ' ' +  template
    cmd_learn += ' ' + input
    cmd_learn += ' ' + model + ' > train_log.txt'
    sys.stdout.write('Begin traing crf model:\n%s\n' % (cmd_learn))
    os.system(cmd_learn)

def make_test_data():
    cmd_test = 'crf_test -m model data/pku_test.utf8.data > test-info.txt'
    os.system(cmd_test)

#python make_crf_model.py -t template -i data/pku_training.utf8.tag -m model
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest = 'template', help="template file", default='template')
    parser.add_argument("-i", dest = 'input',help="train data", default='data/pku_training.utf8.tag')
    parser.add_argument("-m", dest = 'model', help="model file,output file to write.", default='model')
    
    args = parser.parse_args()
    
    crf_train_modle(args.template, args.input, args.model)
