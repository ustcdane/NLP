#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "Annotate/PinyinAnnotator.h"
#include "WordSegmentorForPyAnno/Segmentor/DicTree.h"
#include "WordSegmentorForPyAnno/CommonSegmentor/WordSegmentor.h"
#include "Segmentor.h"

using namespace std;
using namespace NSPinyinAnnotator;

const int   c_max_len = 100;

char  binPath[1024];       
char  dirPath[1024];
char  basePath[1024];
char  dicwrongPath[1024];

int     segResult[c_max_len+1];
string  annoResult;
double  tf;
double  df;

Segmentor*      seg;

/***************************************************************************************
 *                                      SEG Funcions
 ***************************************************************************************/
bool Segment(const char* input){
    int ids[c_max_len];

    if (strlen(input) > c_max_len)
        return false;
    int count = seg->SegmentFast(input, strlen(input), ids);
    if (count == 0)
        return false;

    segResult[0] = count;
    for (int j = 0; j < count; j++)
        segResult[j+1] = ids[count-j-1];

    //check the continues single-hz number
    int single = 0;
    int max_single_len = 0;
    // feng@debug
    //  string recovery="";
    for (int j = 0; j < count; j++){
        if (seg->m_length[segResult[j+1]] == 1){
            if (++ single > max_single_len)
                max_single_len = single;
        }
        else
            single = 0;
        // feng@debug
        //  recovery += seg->m_hz[segResult[j+1]];
    }
    if (max_single_len > 6)
        return false;
    //if (strcmp(recovery.c_str(), input) != 0){
    //    cerr << "Segment Error: " << input << " " << recovery << endl;
    //    return false;
    //}

    return true;
}


/***************************************************************************************
 *                                      ANNO Funcions
 ***************************************************************************************/
bool Annotate(const char* input){
    AnnotateResult annoresult[128];
    bool isexisted = false;
    int r = 0;
    int i = 0;
    int maxid = -1;
    float maxprob = 0;
    char buf[1024];

    r = PinyinAnnotator::instance()->annotateWordBySegmentor(input, annoresult, 128, isexisted);
    if ( r <= 0 )
        return false;

    maxid = -1;
    maxprob = 0;
    for (int j = 0 ; j < r ; ++j ) {
        if ( annoresult[j].power > maxprob ) {
            maxid = j;
            maxprob = annoresult[j].power;
        }
        //@feng:debug
        //cout << annoresult[j].str << endl;
        //cout << annoresult[j].power << endl;
    }
    // feng@bug fixed: when r == 128 and all results' power == 0, error occured
    if (maxid == -1)
        return false;

    EncodingConvertor::getInstance()->sbc2dbc(annoresult[maxid].str.c_str(), buf, 1024);
    annoResult = buf;

    int hz_count=0;
    int py_count=0;
    int pair=0; 
    bool py_flag=false;
    //char tmp[1024];
    //char tmp_py[1024];
    for (int i = 0; i < strlen(buf);){
        if (buf[i] < 'a' || buf[i] > 'z'){
            i += 2;
            //tmp[hz_count++] = buf[i++];
            //tmp[hz_count++] = buf[i++];
            py_flag = false;
        }
        else {
            i++;
            //tmp_py[py_count++] = buf[i++];
            if (!py_flag){
                pair++;
                py_flag = true;
            }
        }
        
    }
    //tmp[hz_count]='\0';
    //tmp_py[py_count]='\0';
    //if (strcmp(tmp, input) != 0 || pair * 2 != strlen(input)){
    if (pair * 2 != strlen(input)){
        cerr << "Annotate Error: " << input << " " << pair << endl;
        return false;
    }

    return true;
}

/***************************************************************************************
 *                                      AUX Funcions
 ***************************************************************************************/
void init(int argc, char* argv[]){
    if ( 5 != argc ) {
        cerr << "ERROR: input parameters error" << endl;
        cerr << "USAGE: ./seganno binPath dirPath basePath dicwrongPath" << endl;
        exit(-1);
    }

    strcpy(binPath, argv[1]);
    strcpy(dirPath, argv[2]);
    strcpy(basePath, argv[3]);
    strcpy(dicwrongPath, argv[4]);

    seg = new Segmentor(basePath, dicwrongPath);
    if (0 != PinyinAnnotator::instance()->open(argv[1], argv[2], NULL, NULL, true)) {
        cerr << "ERROR: annotator init failed.." << endl;
        exit(-1);
    }

}

void deinit(){
    PinyinAnnotator::instance()->clear();
    delete seg;
}

//void dump(){/*{{{*/
//    const char* buf = annoResult.c_str();
//    int   len = strlen(buf);
//    int   cur = 0;
//
//    int count = segResult[0];
//    printf("%.0lf\t%.0lf\t%d", tf, df, count);
//    for (int j = 0; j < count; j++){
//        printf("\t");
//        //feng@add: change output format from mix to hzpy
//        char tmp[1024];
//        int  letterNum = 0;
//        //for (int k = 0; k < seg->m_length[segResult[j+1]]; k++){
//        for (int k = 0; cur < len && k < seg->m_length[segResult[j+1]]; k++){
//            printf("%c", buf[cur++]);
//            printf("%c", buf[cur++]);
//            while (cur < len && buf[cur] >= 'a' && buf[cur] <='z')
//                //fprintf(f, "%c", buf[cur++]);
//                tmp[letterNum++] = buf[cur++];
//            tmp[letterNum++]='\'';
//        }
//        tmp[letterNum] = '\0';
//        printf("%s", tmp);
//    }
//    printf("\n");
//}
/*}}}*/

void dump(){
    const char* buf = annoResult.c_str();
    int   len = strlen(buf);
    int   cur = 0;

    int count = segResult[0];
    printf("%.0lf\t%.0lf\t%d", tf, df, count);
    for (int j = 0; j < count; j++){
        printf("\t");
        //feng@add: change output format from mix to hzpy
        char tmp[1024];
        int  letterNum = 0;
        printf("%s", seg->m_hz_corrected[segResult[j+1]].c_str());
        for (int k = 0; cur < len && k < seg->m_length[segResult[j+1]]; k++){
            //printf("%c", buf[cur++]);
            //printf("%c", buf[cur++]);
            cur+=2;
            while (cur < len && buf[cur] >= 'a' && buf[cur] <='z')
                //fprintf(f, "%c", buf[cur++]);
                tmp[letterNum++] = buf[cur++];
            tmp[letterNum++]='\'';
        }
        tmp[letterNum] = '\0';
        printf("%s", tmp);
    }
    printf("\n");
}

void dump_segment(){
    for (int i = 0; i < segResult[0]; i++){
        cout << seg->m_hz_corrected[segResult[i+1]]  << "\t";
    }
    cout << endl;
}

void dump_annotate(){
    cout << annoResult << endl;

}

/***************************************************************************************
 *                                      MAIN Funcions
 ***************************************************************************************/
int main( int argc, char *argv[] )
{
    init(argc, argv);

    //char phrase[100000];
    string line, phrase;
    int count=0;
    while (getline(cin, line)){
        istringstream iss(line);
        iss >> phrase >> tf >> df;
        
        // feng@debug
        //cout << line << " ";
        //cout << ++count << "\n";
        
        if (!Segment(phrase.c_str()))
            continue;
 ///       if (!Annotate(phrase.c_str()))
            continue;
 ///       dump();

        //if (segResult[0] >= 48){
        //    cout << line << endl;
        //    dump();
        //}
        //if (++count % 1000000 == 0)
        //    cerr << "lines processed: " << count << endl;
    }

    deinit();
    return 0;
}


