#!/bin/sh

# add tag to training data, will generate train data with tag, i.e. data/pku_training.utf8.tag
python addTag.py -i data/pku_training.utf8 -o data/pku_training.utf8.tag -t

# training crf model, will generate crf mode, i.e. model
python make_crf_model.py -t template -i data/pku_training.utf8.tag -m model

# seg  test data, will generate segment data from pku_test.utf8
python crf_segmenter.py -m model -i data/pku_test.utf8 -o  pku_test_seg.txt

# test seg from cmd input
python segment_word_test.py -m model
