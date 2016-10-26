/*=============================================================================
#     FileName: seg_and_pos.cpp
#         Desc: ltp  segment and pos
#       Author: Daniel Wang
#        Email: daneustc@gmail.com
#     HomePage: http://ustcdane.github.io/
#      Version: 0.0.1
#   LastChange: 2016-10-26 19:59:42
#      History:
#    complie: g++ -o seg_and_pos seg_and_pos.cpp -I ../include/ -I../thirdparty/boost/include -L../lib/ -lboost_regex -lsegmentor -lpostagger
#    use:./seg_and_pos ../ltp_data/cws.model ../ltp_data/pos.model 
=============================================================================*/
#include <iostream>
#include <string>
#include <vector>

#include "ltp/segment_dll.h"
#include "ltp/postag_dll.h"

int main(int argc, char * argv[]) {
    if (argc < 3) {
        std::cerr << "[cws model path] [pos model path]" << std::endl;
        return -1;
    }
	
	
	void *engine_seg = segmentor_create_segmentor(argv[1]);
    if (!engine_seg) {
        std::cerr << "cws model path load error!!" << std::endl;
        return -1;
    }

    void * engine_pos = postagger_create_postagger(argv[2]);
    if (!engine_pos) {
        std::cerr << "pos model path load error!!" << std::endl;
        return -1;
    }

    std::vector<std::string> words;
	std::vector<std::string> tags;
	
	std::string line;
	while(getline(std::cin, line)) {
		if(line.length() == 0)
			continue;
		words.clear();
		tags.clear();

		int len = segmentor_segment(engine_seg, line.c_str(), words);//分词接口，对句子分词
		std::cout<<"segs: "<< len <<"\twords len:"<<words.size()<< std::endl;
		for(int i=0; i < len; ++i) 
			std::cout<< words[i] << "|";
		std::cout<<"\n";
			
		postagger_postag(engine_pos, words, tags);// 词性标注接口
		for (int i = 0; i < tags.size(); ++ i) {
			std::cout << words[i] << "/" << tags[i];
			if (i == tags.size() - 1) 
				std::cout << std::endl;
			else 
				std::cout << " ";
		}
	}
	
	segmentor_release_segmentor(engine_seg);//分词接口，释放分词器
    postagger_release_postagger(engine_pos);// 释放词性标注接口‘

    return 0;
}

