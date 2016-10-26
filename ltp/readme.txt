
ltp分词及词性标注测试：
把seg_and_pos.cpp 放入目录 ltp-3.3.2/examples

编译：
g++ -o seg_and_pos seg_and_pos.cpp -I ../include/ -I../thirdparty/boost/include -L../lib/ -lboost_regex -lsegmentor -lpostagger

运行：
./seg_and_pos ../ltp_data/cws.model ../ltp_data/pos.model

ref: 
http://ltp.readthedocs.io/zh_CN/latest/