
ltp�ִʼ����Ա�ע���ԣ�
��seg_and_pos.cpp ����Ŀ¼ ltp-3.3.2/examples

���룺
g++ -o seg_and_pos seg_and_pos.cpp -I ../include/ -I../thirdparty/boost/include -L../lib/ -lboost_regex -lsegmentor -lpostagger

���У�
./seg_and_pos ../ltp_data/cws.model ../ltp_data/pos.model

ref: 
http://ltp.readthedocs.io/zh_CN/latest/