#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "Segmentor.h"

using namespace std;
// gb18030 encoding
const int   c_max_len = 128;

char  basePath[1024];

int     segResult[c_max_len + 1];
double  tf;
double  df;

Segmentor*      seg;

bool Segment(const char* input) {
	int ids[c_max_len];

	if (strlen(input) > c_max_len)
		return false;
	int count = seg->SegmentFast(input, strlen(input), ids);
	if (count == 0)
		return false;

	segResult[0] = count;
	for (int j = 0; j < count; j++)
		segResult[j + 1] = ids[count - j - 1];

	//check the continues single-hz number
	int single = 0;
	int max_single_len = 0;

	for (int j = 0; j < count; j++) {
		if (seg->hzLength_[segResult[j + 1]] == 1) {
			if (++single > max_single_len)
				max_single_len = single;
		}
		else
			single = 0;
	}
	if (max_single_len > 6)
		return false;

	return true;
}

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

void dump_segment() {
	for (int i = 0; i < segResult[0]; i++) {
		cout << seg->hz_[segResult[i + 1]] << "\t";
	}
	cout << endl;
}

int main(int argc, char *argv[])
{
	init(argc, argv);

	string line, phrase;
	int count = 0;
	while (getline(cin, line)) {
		istringstream iss(line);
		iss >> phrase >> tf >> df;

		if (!Segment(phrase.c_str()))
			continue;
		///dump_segment();
	}

	deinit();
	while (1)
	{
		;
	}
	return 0;
}


