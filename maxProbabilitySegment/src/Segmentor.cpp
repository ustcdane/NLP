#include "Segmentor.h"

int Segmentor::SegmentFast(const char* word, int len, int* rIndexs) {
	int pre [len+1];
	int prob[len+1];
    VocabIndex id_list[len+1];
    VocabIndex id;
	
	memset(pre, -1, sizeof(pre));
	memset(prob,1000000,sizeof(prob));

	pre[0] = 0;
	prob[0] = 0;
	
	printf("----------- %s ----------\n", word);// by wangdan
	for(int i = 0; i < len-1 ; i+= 2){
		if (pre[i] == -1){
			continue;
		}
		for(int j = i+2; j <= len; j+=2){
			if (j - i > m_longest){
				break;
			}
            string tmp(word+i, j-i);
            if (m_hash.find(tmp) != m_hash.end())
                id = m_hash[tmp];
            else 
                continue;
			int vl =(int)( c_punish + m_lograte[id]) + prob[i];
			printf("%d\t%s\t%d\t%d\n", i, tmp.c_str(), int(m_lograte[id]), vl);// by wangdan
			if (vl < prob[j]){
				prob[j] = vl;
				pre [j] = i;
                id_list[j] = id;
			}
		}
	}
    int count = 0;
	for(int i = len; i > 0; ){
		if ( pre[i] == -1){
			return 0;
		}
        rIndexs[count++] = id_list[i];
		i = pre[i];
	}
	
	printf("\nsegment res:\n"); // by wangdan
	// dump segment result by wangdan
	int segResult[129] = {0};
	segResult[0] = count;
	for (int j=0; j < count; j++ )
		segResult[j+1] = rIndexs[count-j-1];
	
	for (int j=0; j < count; j++ )
		printf("%s ", m_hz_corrected[segResult[j+1]].c_str());
	printf("\n");

	return count;
}

