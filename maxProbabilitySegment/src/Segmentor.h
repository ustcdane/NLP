#pragma once

#include <cstdio>
#include <cmath>
#include <cstring>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

#define SENTENCE_MAX_LEN (1024+1)
#define DEBUG_INFO 1

typedef int  VocabIndex;
typedef double VocabFreq;
typedef unordered_map<string, VocabIndex> SIMAP;// word index
typedef unordered_map<string, VocabIndex>::iterator SIMAP_IT;

class Segmentor {
public:
	const static double c_punish;
	const static double c_logmin;
	const static int    c_max;
	const static double c_stop;
	const static int    c_dic_maxlen;
	const static int    c_dic_maxsize;

public:
	Segmentor(const char* dic_name):dictSize_(0), hzLongest_(0) {
		hz_.push_back("");
		hzFreq_.push_back(0);
		hzLength_.push_back(0);

		load_dic(dic_name);
		calcProbability();
	}
	~Segmentor() {}
	int SegmentFast(const char* words, int len, int* r_ids);

private:
	void load_dic(const char* dicname) {
		fstream fin(dicname, ios::in);
		if (!fin) {
			cerr << "ERROR: cannot open dic file " << dicname << endl;
			exit(-1);
		}

		string line;
		string hz;
		VocabFreq freq;

		dictSize_ = 0;
		while (getline(fin, line)) {
			istringstream iss(line);
			iss >> hz >> freq;
			if (hz.length() > c_dic_maxlen)
				continue;
			if (hzIdHash_.find(hz) != hzIdHash_.end()) {
				cerr << "ERROR: dup in dic " << hz << endl;
				exit(-1);
			}

			++dictSize_;
			hzIdHash_[hz] = dictSize_;
			hz_.push_back(hz);
			hzLength_.push_back(hz.length() / 2);
			hzFreq_.push_back(freq);
			hzFreq_[0] += freq;// total freq

			if (hz.length() > hzLongest_)
				hzLongest_ = hz.length();
		}

		fin.close();
	}

	void test_dic() {
		for (int i = 1; i <= dictSize_; i++) {
			cout << hz_[i] << "\t" << hzFreq_[i] << endl;
		}
	}

	void calcProbability() { // calc word probability in dict
		hzProb_.resize(dictSize_ + 1);
		hzLogProb_.resize(dictSize_ + 1);

		for (int id = 1; id <= dictSize_; id++) {
			hzProb_[id] = (hzFreq_[id] + 1.0) / (hzFreq_[0] + dictSize_); // add one smooth
			hzLogProb_[id] = log(hzProb_[id]) / log(0.985);
		}
	}

public:
	vector<string>      hz_;
	vector<int>         hzLength_;
private:
	SIMAP               hzIdHash_;     // To store the dict. <word, index>
	vector<VocabFreq>   hzFreq_;       // word freq
	int                 dictSize_;     // dict size
	int                 hzLongest_;   // longest length of word in dict.
	vector<double>      hzProb_;		    // store each word probability
	vector<double>      hzLogProb_;	    // store each word log(probability)
};