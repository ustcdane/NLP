#include "Segmentor.h"

const double Segmentor::c_punish = 198;
const double Segmentor::c_logmin = 100000;
const int    Segmentor::c_max = (unsigned short)(-1);
const double Segmentor::c_stop = 300;
const int    Segmentor::c_dic_maxlen = 512;
const int    Segmentor::c_dic_maxsize = 500000;

int Segmentor::SegmentFast(const char* word, int len, int* rIndexs) {
	int pre[SENTENCE_MAX_LEN];// 前驱节点
	int prob[SENTENCE_MAX_LEN];// 记录当前最大的概率累加值(概率对数对应的是最小值)
	VocabIndex id_list[SENTENCE_MAX_LEN];
	VocabIndex id;

	memset(pre, -1, sizeof(pre));
	memset(prob, 1000000, sizeof(prob));

	pre[0] = 0;
	prob[0] = 0;
#ifdef DEBUG_INFO
	printf("----------- %s ----------\n", word);
	printf("pos\tword\tlogProbility\tsumProb\n");
#endif // DEBUG_INFO

	for (int i = 0; i < len - 1; i += 2) {
		if (pre[i] == -1) {
			continue;
		}
		for (int j = i + 2; j <= len; j += 2) {
			if (j - i > hzLongest_) {
				break;
			}
			string tmp(word + i, j - i);
			if (hzIdHash_.find(tmp) != hzIdHash_.end())
				id = hzIdHash_[tmp];
			else
				continue;
			int vl = (int)(c_punish + hzLogProb_[id]) + prob[i];
#ifdef DEBUG_INFO
			printf("%d\t%s\t%d\t%d\n", i, tmp.c_str(), int(hzLogProb_[id]), vl);
#endif 
			if (vl < prob[j]) {
				prob[j] = vl;
				pre[j] = i;
				id_list[j] = id;
			}
		}
	}
	int count = 0;
	for (int i = len; i > 0; ) {
		if (pre[i] == -1) {
			return 0;
		}
		rIndexs[count++] = id_list[i];
		i = pre[i];
	}

#ifdef DEBUG_INFO
	// dump segment result
	printf("\nsegment res:\n");						
	int segResult[129] = { 0 };
	segResult[0] = count;
	for (int j = 0; j < count; j++)
		segResult[j + 1] = rIndexs[count - j - 1];

	for (int j = 0; j < count; j++)
		printf("%s ", hz_[segResult[j + 1]].c_str());
	printf("\n");

#endif // DEBUG_INFO
	return count;
}