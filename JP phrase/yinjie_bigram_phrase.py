#coding:gb18030
import os


_get_abs_path = lambda path: os.path.normpath(os.path.join(os.getcwd(), path))

DEFAULT_DICT = _get_abs_path("jp_bi.txt")


class Tokenizer(object):
    def __init__(self, dictionary=DEFAULT_DICT):
        self.dictionary = _get_abs_path(dictionary)
        self.UniSet = set()
        self.BiDict = {}
        self.route = {}
        self.initialized = False
        
    def get_dict(self, f_name):
        bi_id = ''
        print f_name
        with open(f_name, 'rb') as f:
            for lineno, line in enumerate(f, 1):
                try:
                    line = line.strip()
                    segs = line.split('\t')

                    if len(segs) == 2:# jp bigram lef right
                        self.UniSet.add(segs[0])
                        self.UniSet.add(segs[1])
                        bi_id = line
                    if len(segs) == 3: # yinjie bigram
                        if bi_id not in self.BiDict:
                            self.BiDict[bi_id] = [(segs[0],segs[1],segs[2])]
                        else:
                            self.BiDict[bi_id].append((segs[0], segs[1], segs[2]))
                except ValueError:
                    raise ValueError(
                        'invalid dictionary entry in %s at Line %s: %s' % (f_name, lineno, line))

    def check_initialized(self):
        if not self.initialized:
            abs_path = _get_abs_path(self.dictionary)
            self.get_dict(abs_path)
            # 标记初始化成功
            self.initialized = True

    def get_DAG(self, sentence):
        self.check_initialized()
        DAG = {}
        N = len(sentence)
        for k in xrange(N):
            tmplist = []
            i = k
            frag = sentence[k]
            while i < N and frag in self.UniSet:
                if frag in self.UniSet:
                    tmplist.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not tmplist:
                tmplist.append(k)
            DAG[k] = tmplist
        return DAG


    #动态规划，计算最大概率的切分组合
    def calc(self, sentence, DAG, route):
        N = len(sentence)
        route[N] = [(0, 0, 0)] # 每个节点记录当前节点得分及其对应的末尾节点位置,及下一个节点列表的后驱位置

        MAX = 99999999
        for i in xrange(N):
            route[i] = [(MAX, N-1, 0)]
        '''
        route={0: [(99999999, 3, 0), (956, 1, 0)],
        1: [(0, 3, 0), (735, 1, 0)],
         2: [(0, 3, 0), (797, 2, 0)],
         3: [(0, 3, 0)],
         4: [(0, 0, 0)]}

        route[idx] = [min([ (得分，词语末字位置,二元对应的右元位置)])]
        以idx:(得分，词语末字位置)键值对list形式保存在route中
        route[x+1][...][0] 表示 词路径[x+1,N-1]的最好的得分序列,
        [x+1][0][0]即表示取句子x+1位置对应元组(得分，词语末字位置,二元对应的右元位置)的得分
        [x+1][0][1]即表示取句子x+1位置对应元组(得分，词语末字位置,二元对应的右元位置)的词语末尾位置
         '''

        # 从后往前遍历句子 反向计算最大概率
        for idx in xrange(N - 1, -1, -1):
            cost = MAX
            pos = N
            next_node_pos = 0
            #print idx
            for x in DAG[idx]:
                left = sentence[idx:x + 1]
                if left not in self.UniSet:
                    continue
                if x+1 == N:
                    route[idx][0] = (0, N-1, 0)
                  #  print  'R:', left,idx,N-1
                    continue
                for index, idx_path in enumerate(route[x + 1]):# 遍历右元对应的节点列表
                    right_end_index = N if idx_path[1]+1 >= N else  idx_path[1]+1
                    right_begin_index = x+1
                #    print left,x,right_begin_index,right_end_index

                    right = sentence[right_begin_index :right_end_index]
                    if right not  in self.UniSet:
                        continue
                    bi_v = MAX
                    bi_id = left + '\t' + right

                    if bi_id in self.BiDict:
                        bi_v = int(self.BiDict[bi_id][0][2])
                    #    print bi_id,bi_v,right_begin_index,route[x+1][0]
                    if cost > idx_path[0] + bi_v:
                        cost = idx_path[0] + bi_v
                        pos = x
                        next_node_pos = index
                      #  print 'debug:pre node pos: %d pre cost:%d cost:%d left:%s\tright:%s' % \
                    #        (index, idx_path[0], cost, left, right)
         #   print "before update idx %d route:" % (idx)
       #     for it in route[idx]:
         #       print '\tmin_cost:%d, best pos:%d' % (it[0], it[1])
            if pos < N: # get the best
                route[idx].append((cost, pos, next_node_pos))
           #     print 'update route:',idx, cost,pos
                                                      
    # DAG中是以{key:list,...}的字典结构存储
    # key是字的开始位置

    def cut_DAG_Result(self, sentence):
        DAG = self.get_DAG(sentence)
        route = self.route
        self.calc(sentence, DAG, route)
        x = 0
        N = len(sentence)
        l_word = ''
        start_node = route[0]
        next_node = start_node[start_node.index(min(start_node))]
        while x < N:
            y = next_node[1] + 1
            l_word = sentence[x:y]# 得到以x位置起点的最大概率切分词语
            if l_word:
                yield l_word
                x = y
                next_node = route[x][next_node[2]]


    def get_pys(self, segs):
        segs_len = len(segs)
        if segs_len < 2:
            return segs[0]

        pys = ''
        left_yinjie = ''
        right_yinjie = ''
        for i in xrange(1, segs_len):
            left = segs[i-1]
            right = segs[i]
            bi_id = left + '\t' + right

            if bi_id in self.BiDict:
                left_yinjie = self.BiDict[bi_id][0][0]
                right_yinjie = self.BiDict[bi_id][0][1]
                pys += left_yinjie
        if right_yinjie:
            pys += right_yinjie
        return pys




if __name__ == '__main__':
    s = 'tjdx'
    t = Tokenizer()

    res = list(t.cut_DAG_Result(s))
    #print('/'.join(res))
    print t.get_pys(res)
    print t.route
