#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "Segmentor.h"

using namespace std;

const int   c_max_len = 128;
char  basePath[1024];
Segmentor*      seg;

void init(int argc, char* argv[]) {
	if (2 != argc) {
		cerr << "ERROR: input parameters error" << endl;
		cerr << "USAGE: ./seganno basePath dicwrongPath" << endl;
		exit(-1);
	}

	strcpy(basePath, argv[1]);

	seg = new Segmentor(basePath);
}

void deinit() {
	delete seg;
}

int main(int argc, char *argv[])
{
	init(argc, argv);

	string line, sentence;
	int count = 0;
	while (getline(cin, line)) {
		istringstream iss(line);
		iss >> sentence;
		std::vector<std::string> res;
		if (!seg->SegmentWrap(sentence, res))
			continue;
		std::cout << sentence << "\tsegment result:\n";
		for (int i=0 ; i < res.size(); ++i) {
			std::cout << res[i] << "\t";
		}
		std::cout << "\n";
	}

	deinit();
	getchar();
	return 0;
}


