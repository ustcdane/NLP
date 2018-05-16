#!/bin/sh

\rm *\.o
#swig -python weights_compress.i
g++ -O3 -mavx2 -Wno-cpp -std=c++11 -fopenmp -fPIC -c weights_compress.cpp weights_compress_wrap.c -I/usr/local/include/ -I/usr/include/python2.7/ -I/search/local_config_python/numpy_include -I.
g++ -fopenmp -shared weights_compress.o weights_compress_wrap.o -o _weights_quantization.so
