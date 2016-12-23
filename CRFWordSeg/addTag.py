#coding:utf-8

import codecs
import sys
import argparse

def tagFile(origin, tagfile, isTrain = True):
    f = codecs.open(origin, 'r', 'utf-8')
    contents = f.read()
    
	taglist = tagText(contents, isTrain)
    fw = codecs.open(tagfile,'w','utf-8')
    fw.write(''.join(taglist))
    fw.close

def tagText(text, isTrain = False):#segment is 
    #try:
     #   text.decode('utf8')
    #except UnicodeDecodeError :
     #   sys.stderr.write("tagText Error! input not utf8 encode.")
      #  return []
    text = text.replace(u'\r',u'')
    text = text.replace(u'\n',u' \n ')
    words = text.split(' ') if isTrain else list(text)
    
    # tagword is the chinese word after beging taged,
    # i.e. "中国" -> "中 CN B" "国 CN E"
    taglist = []
    
    for word in words:
        if len(word) == 0:
            continue
        elif len(word) == 1:
            if word == u'\n':
                tagword = u'\n'
            elif word == u' ':
                continue
            else:
                tagword = word + featureTag(word) + ' S' + u'\n'
        elif len(word) == 2:
            tagword = word[0] + featureTag(word[0]) + ' B' + u'\n' + word[1] + featureTag(word[1]) + ' E' + u'\n'
        else:
            tagword = word[0] + featureTag(word[0]) + ' B' + u'\n'
            for midword in word[1 : -1]:
                tagword += midword + featureTag(midword) + ' M' + u'\n'
            tagword += word[-1] + featureTag(word[-1]) + ' E' + u'\n'
        taglist.append(tagword)
    return taglist

def featureTag(word):
    
    punc = [u'，', u',', u'"', u'“', u'”', u'、', u'：',  u'。', u'！', u'？', u'（', u'）', u'：', u'《', u'》', u'-', u'-', u'%', u'*', u'/', u'.', u'°']
    num = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'0',
           u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'○' ,u'零', u'个', u'十', u'百', u'千', u'万', u'亿']
    time = [u'年', u'月', u'日', u'时', u'分', u'秒']
    if word in punc:
        return ' PUNC'
    elif word in num:
        return ' NUM'
    elif word in time:
        return ' TIM'
    else:
        return ' CN'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest = 'input',help="input file to tag.")
    parser.add_argument("-o", dest = 'output', help="output file to write.")
    parser.add_argument("-t", dest = 'bTrain', action='store_true',help="Will training mode ...")
    args = parser.parse_args()
    #print args
    tagFile(args.input, args.output, args.bTrain)

