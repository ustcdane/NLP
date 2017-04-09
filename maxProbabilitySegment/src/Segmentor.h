#ifndef _SEGMENTER_
#define _SEGMENTER_

#include <cstdio>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <tr1/unordered_map>

using namespace std;

typedef int  VocabIndex;
typedef double VocabFreq;
typedef tr1::unordered_map<string, VocabIndex> SIMAP;
typedef tr1::unordered_map<string, VocabIndex>::iterator SIMAP_IT;

class Segmentor{
public:
	const static double c_punish = 198;
	const static double c_logmin = 100000;
	const static int    c_max    = (unsigned short)(-1);
	const static double c_stop = 300;
    const static int    c_dic_maxlen = 512;
    const static int    c_dic_maxsize = 500000;

public:
	Segmentor(const char* dic_name, const char* dicwrong_name){
        m_hash.clear(); 
        m_hz.clear();   m_hz.push_back("");
        m_freq.clear(); m_freq.push_back(0);
        m_length.clear(); m_length.push_back(0);
        m_dicsize = 0;  m_longest = 0;
        
        load_dic(dic_name);
        load_dicwrong(dicwrong_name);
        calc_rate();
	}
	~Segmentor(){}
	int SegmentFast(const char* words, int len, int* r_ids);

private:
    void load_dic(const char* dicname){
        fstream fin(dicname, ios::in);
        if (!fin){
            cerr << "ERROR: cannot open dic file " << dicname << endl;
            exit(-1);
        }

        string line;
        string hz;
        VocabFreq freq;

        m_dicsize = 0;
        while (getline(fin, line)){
            istringstream iss(line);
            iss >> hz >> freq;
            if (hz.length() > c_dic_maxlen)
                continue;
            if (m_hash.find(hz) != m_hash.end()){
                cerr << "ERROR: dup in dic " << hz << endl;
                exit(-1);
            }

            ++m_dicsize;
            m_hash[hz] = m_dicsize;
            m_hz.push_back(hz);
            m_length.push_back(hz.length()/2);
            m_freq.push_back(freq);
            m_freq[0] += freq;

            if (hz.length() > m_longest)
                m_longest = hz.length();
        }

        fin.close();

        // 2012年10月24日增加 为了把错词词频加回到正确词的词频
        m_hz_corrected = m_hz;
    }

    void load_dicwrong(const char* dicname){
        fstream fin(dicname, ios::in);
        if (!fin){
            cerr << "ERROR: cannot open dic file " << dicname << endl;
            exit(-1);
        }

        string line;
        while (getline(fin, line)){
            istringstream iss(line);
            string hz_wrong, hz_corrected;
            iss >> hz_wrong >> hz_corrected;
            if (hz_wrong.length() == hz_corrected.length() && m_hash.find(hz_wrong) != m_hash.end()){
                int index=m_hash[hz_wrong];
                m_hz_corrected[index] = hz_corrected;
                //cout << hz_wrong << " -> " << hz_corrected << endl;
            }
        }

        fin.close();
    }

    void test_dic(){
        for (int i = 1; i <= m_dicsize; i++){
            cout << m_hz[i] << "\t" << m_freq[i] << endl;
        }
    }

	void calc_rate(){
        m_rate.resize(m_dicsize + 1);
        m_lograte.resize(m_dicsize + 1);
		
		for(int id = 1; id <= m_dicsize; id++){
			m_rate[id] = (m_freq[id]+1.0) / (m_freq[0]+m_dicsize);
			m_lograte[id] = log(m_rate[id]) / log(0.985);
		}
	}
    
public:
    SIMAP               m_hash;     // data structures to store the dic
    vector<string>      m_hz;
    vector<string>      m_hz_corrected; // 加入了dic_wrong里面的信息。
    vector<int>         m_length;
    vector<VocabFreq>   m_freq;
    int                 m_dicsize;     // dic size
    int                 m_longest;  // longest length of word in dic.
    
	vector<double>      m_rate;		    // store each probability
	vector<double>      m_lograte;	    // store each log(probability)
};

#endif
