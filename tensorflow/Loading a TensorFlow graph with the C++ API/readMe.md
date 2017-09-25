- Creating a minimal TensorFlow graph and write it out as a protobuf file
-  Loading a TensorFlow graph with the C++ API, steps as:
```
Initialize a TensorFlow session.
Read in the graph we exported above.
Add the graph to the session.
Setup our inputs and outputs.
Run the graph, populating the outputs.
Read values from the outputs.
Close the session to release resources.
 ```


>
 https://medium.com/jim-fleming/loading-a-tensorflow-graph-with-the-c-api-4caaff88463f
 https://github.com/tensorflow/tensorflow/tree/master/tensorflow/core/public