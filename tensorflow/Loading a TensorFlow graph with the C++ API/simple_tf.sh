
g++ -std=c++11 -o tf_simple_cpp_demo -I./tf -I./eigen -g -Wall -D_DEBUG -Wshadow -Wno-sign-compare -w -I./proto/include  -pthread -L./proto/lib -lprotobuf -lpthread -L./ -ltensorflow_cc load_tf_mode.cpp
