#coding:utf8

from crf_segmenter import crf_segment
import sys
import CRFPP
import argparse

#python segment_word_test.py -m model
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-m", dest = 'model',help=" model file")
	args = parser.parse_args()
	sys.stdout.write('please utf8 string to segment, blank line to stop.\n')
	print args
	tagger = CRFPP.Tagger("-m " + args.model)
	
	while True:
		line = raw_input('input utf8 sentence:\n')
		line = line.strip()
		if not len(line):
			break
		line = line.decode('utf8')
		#print line
		tagger.clear()
		resList = crf_segment(line, tagger)
		print 'seg:\n',(u' '.join(resList)).encode('utf8')

