#coding:utf-8

'''
CRF Segmenter based character tagging:
4 tags for character tagging: B(Begin), E(End), M(Middle), S(Single)

'''

import codecs
import sys
from addTag import tagText
import CRFPP
import argparse

def crf_segmenter_file(input_file, output_file, tagger):
    input_f = codecs.open(input_file, 'r', 'utf-8')
    output_f = codecs.open(output_file, 'w', 'utf-8')

    input_data = input_f.readlines()
    for line in input_data:
        result = crf_segment(line, tagger)
        for word in result[:-1]:
            word += u' '
            output_f.write(word)
        if len(result):
            output_f.write(result[-1])
            output_f.write('\n')
    
    input_f.close()
    output_f.close()

def crf_segment(line, tagger):
    result = []
    tagger.clear()
    line = line.strip()
    wordListWithTag = tagText(line)
    for word in wordListWithTag:
        if word:
            tagger.add(word.encode('utf8'))

    tagger.parse()
    size = tagger.size()
    xsize = tagger.xsize()
    
    segWord = u''
    for i in range(0, size):
        #for j in range(0, xsize):
        if xsize:
            char = tagger.x(i, 0).decode('utf-8')
            tag = tagger.y2(i)
            #print char, tag
            segWord += char
            if tag in ('S', 'E'):
                result.append(segWord)
                segWord = u''
    return result

#python crf_segmenter.py -m model -i data/pku_test.utf8 -o pku_test_seg.txt
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", dest = 'model',help=" model file")
    parser.add_argument("-i", dest = 'input',help="input file to tag.")
    parser.add_argument("-o", dest = 'output', help="output file to write.")
    
    #if len(sys.argv) != 7:
     #   print "pls use: python crf_segmenter.py -m model -i input -o output"
      #  sys.exit(1)
    
    args = parser.parse_args()

    tagger = CRFPP.Tagger("-m " + args.model)
    crf_segmenter_file(args.input, args.output, tagger)
