#include "Segmentor.h"

const double Segmentor::c_punish = 198;
const double Segmentor::c_logmin = 100000;
const int    Segmentor::c_max = (unsigned short)(-1);
const double Segmentor::c_stop = 300;
const int    Segmentor::c_dic_maxlen = 512;
const int    Segmentor::c_dic_maxsize = 500000;
const int    Segmentor::c_max_len = 256;

Segmentor* Segmentor::ins_ = nullptr;

Segmentor* Segmentor::instance(const char* dic_name){
  if(!ins_){
        ins_ = new Segmentor(dic_name);
  }
  return ins_;
}


bool isGBKHZ(unsigned short wc) { // gb18030 has two char
	unsigned char paramlow = wc & 0xFF;
	unsigned char paramhigh = wc >> 8;
	bool flag = false;
	if (((paramlow >= 0xB0 && paramlow <= 0xF7) && (paramhigh >= 0xA1 && paramhigh <= 0xFE))
		|| ((paramlow >= 0x81 && paramlow <= 0xA0) && (paramhigh >= 0x40 && paramhigh < 0xFE))
		|| ((paramlow >= 0xAA && paramlow <= 0xFE) && (paramhigh >= 0x40 && paramhigh <= 0xA0)))
		flag = true;
	return flag;
}

typedef struct sentenceSegs{
	std::string sentence_;// 句子
	bool isZh_; 
	sentenceSegs(const std::string &sen, bool isZh = false):sentence_(sen), isZh_(isZh){}
}sentenceSegs_t;


void preProcessSen(const char* word, int len, std::vector<sentenceSegs_t> &sentenceVec) {
	std::string temp;
	bool isGbk = true;
	for (int i = 0; i < len;) {
		if (isGBKHZ(*(unsigned short*)(word + i))) { // get gbk sentence
			if (!isGbk && !temp.empty()) {
				sentenceVec.push_back(sentenceSegs_t(temp, isGbk));
				temp.clear();
			}
			isGbk = true;
			temp.push_back(word[i]);
			temp.push_back(word[i + 1]);
			i += 2;
		} // if gbk
		else {
			if (isGbk && !temp.empty()) {
				sentenceVec.push_back(sentenceSegs_t(temp, isGbk));
				temp.clear();
			}
			isGbk = false;
			// ascii, only has one char
			if (-1 < word[i] && word[i] < 127) {
				temp.push_back(word[i]);
				i += 1;
			} // other
			else {
				temp.push_back(word[i]);
				temp.push_back(word[i + 1]);
				i += 2;
			}
		} // else not gbk
	} // for
	if (!temp.empty()) {
		sentenceVec.push_back(sentenceSegs_t(temp, isGbk));
	}
}


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

			std::string tmp(word + i, j - i);
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
	printf("\n%s\tsegment res:\n", word);
	int segResult[129] = { 0 };
	segResult[0] = count;
	for (int j = 0; j < count; j++)
		segResult[j + 1] = rIndexs[count - j - 1];

	for (int j = 0; j < count; j++)
		printf("%s ", hz_[segResult[j + 1]].c_str());
	printf("\n--------------------------------------\n");

#endif // DEBUG_INFO
	return count;
}

bool Segmentor::Segment(const std::string &input, std::vector<std::string> &res) {
	int ids[c_max_len] = {0};
	int     segResult[c_max_len + 1] = {0};
	if (input.length() > c_max_len)
		return false;
	int count = this->SegmentFast(input.c_str(), input.length(), ids);
	if (count == 0)
		return false;

	segResult[0] = count;
	for (int j = 0; j < count; j++)
		segResult[j + 1] = ids[count - j - 1];

	//check the continues single-hz number
	int single = 0;
	int max_single_len = 0;

	for (int j = 0; j < count; j++) {
		if (this->hzLength_[segResult[j + 1]] == 1) {
			if (++single > max_single_len)
				max_single_len = single;
		}
		else
			single = 0;
	}
/*	if (max_single_len > 6)
		return false;
*/
	for (int i = 0; i < segResult[0]; i++) {
		//std::cout << this->hz_[segResult[i + 1]] << "\t";
		res.push_back(this->hz_[segResult[i + 1]]);
	}

return true;
}

int Segmentor::SegmentWrap(const std::string &sentence, std::vector<std::string> &res) {
	std::vector<sentenceSegs_t> segs;
	preProcessSen(sentence.c_str(), sentence.length(), segs);

#ifdef DEBUG_INFO
	std::cout << "preProcess result:\n--------------------------------------- \n";
	for (int i=0; i < segs.size(); ++i)
		std::cout << segs[i].sentence_ << "\t";
	std::cout << "\n----------------------------------------\n";
#endif

	int totalCount = 0;
	std::vector<std::string> senVec;
	for (int i = 0; i < segs.size(); ++i) {
		if (!segs[i].isZh_) {
			res.push_back(segs[i].sentence_);
			totalCount++;
		}
		else if (Segment(segs[i].sentence_, senVec)) {
			res.insert(res.end(), senVec.begin(), senVec.end());
			totalCount += senVec.size();
			senVec.clear();
		}
	}
	return totalCount;
}
