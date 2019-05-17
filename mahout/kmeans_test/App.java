package com.sogou.ime.mahout.practice;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.Text;
import org.apache.mahout.clustering.Cluster;
import org.apache.mahout.clustering.iterator.ClusterWritable;
import org.apache.mahout.clustering.kmeans.KMeansDriver;
import org.apache.mahout.clustering.kmeans.Kluster;
import org.apache.mahout.common.distance.EuclideanDistanceMeasure;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.Vector;
import org.apache.mahout.math.VectorWritable;
import org.apache.mahout.math.NamedVector;
import org.apache.mahout.clustering.classify.WeightedPropertyVectorWritable; 

public class App {
	 private static final String HDFS = "hdfs://10.129.250.52:9000";
	public static final double[][] points = {
		{1, 1}, {2, 1}, {1, 2},
		{2, 2}, {3, 3}, {8, 8},
		{9, 8}, {8, 9}, {9, 9}};
 

		//public static void writePointsToFile(List<Vector> points,String fileName,FileSystem fs, Configuration conf) throws IOException {
		@SuppressWarnings("deprecation")
		public static void writePointsToFile(List<NamedVector> points,String fileName,FileSystem fs, Configuration conf) throws IOException {
			Path path = new Path(fileName);
			SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf,path, Text.class, VectorWritable.class);
			//long recNum = 0;
			VectorWritable vec = new VectorWritable();
			//for (Vector point : points) {
			for (NamedVector point : points) {
				vec.set(point);
				//writer.append(new LongWritable(recNum++), vec);
				writer.append(new Text(point.getName()), vec);
			}
			writer.close();
		}
 
		//public static List<Vector> getPoints(double[][] raw) {
		public static List<NamedVector> getPoints(double[][] raw) {
			//List<Vector> points = new ArrayList<Vector>();
			List<NamedVector> points = new ArrayList<NamedVector>();
			for (int i = 0; i < raw.length; i++) {
			double[] fr = raw[i];
			Vector vec = new RandomAccessSparseVector(fr.length);
			vec.assign(fr);
			NamedVector vecName;
			vecName = new NamedVector(vec, "Item_No_" + i);
			points.add(vecName);
			}
			return points;
		}
		@SuppressWarnings("deprecation")
		public static void main(String args[]) throws Exception {
			System.setProperty("HADOOP_USER_NAME", "wangdan209498");
		int k = 2;
		//List<Vector> vectors = getPoints(points);//根据初始点坐标数组构建成为聚类算法能够处理的vector的list集合格式
		List<NamedVector> vectors = getPoints(points);//根据初始点坐标数组构建成为聚类算法能够处理的vector的list集合格式
		Configuration conf = new Configuration();
		  /* 
		    conf.addResource("classpath:/hadoop/core-site.xml");
	        conf.addResource("classpath:/hadoop/hdfs-site.xml");
	        conf.addResource("classpath:/hadoop/mapred-site.xml");
	        */
	    FileSystem fs = FileSystem.get(new URI("hdfs://10.129.250.52:9000/"), conf, "/");
		writePointsToFile(vectors, "/clustering/testdata/points/file1", fs, conf);//将点的集合写到hdfs上的数据文件中名称为file1
 
		Path path = new Path("/clustering/testdata/clusters/part-00000");//序列化文件的路径
		@SuppressWarnings("deprecation")
		SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf, path, Text.class, Kluster.class);
		
		// 初始化中心点k=2
		 
		for (int i = 0; i < k; i++) {
		Vector vec = vectors.get(i);
		//cluster--{"r":[],"c":[1.0,1.0],"n":0,"identifier":"CL-0"}
		Kluster cluster = new Kluster(vec, i, new EuclideanDistanceMeasure());
		writer.append(new Text(cluster.getIdentifier()), cluster);
		}
		
		writer.close();
		//运行聚类算法
		KMeansDriver.run(conf,
		new Path(HDFS+"/clustering/testdata/points"),//原始输入
		new Path(HDFS+"/clustering/testdata/clusters/part-00000"),//初始中心点集合
		new Path(HDFS+"/clustering/output"),//聚类结果
		0.001,
		3,
		true,
		0,
		false);
		
		////////////////////////////////////////////////////
		// 从HDFS上读取聚类结果
		//@SuppressWarnings("deprecation")
		SequenceFile.Reader reader = new SequenceFile.Reader(fs,
		new Path("/clustering/output/" +Cluster.CLUSTERS_DIR+"3"+ Cluster.FINAL_ITERATION_SUFFIX + "/part-r-00000"), conf);
		IntWritable key = new IntWritable();
		ClusterWritable value=new ClusterWritable();
		while (reader.next(key, value)) {
		System.out.println(value.getValue().toString() + " belongs to cluster " + key.toString());
		}
		reader.close();
		
		reader = new SequenceFile.Reader(fs, new Path("/clustering/output/" +  Cluster.CLUSTERED_POINTS_DIR + "/part-m-00000"), conf);  
	
		//将分组信息写到文件uidOfgrp.txt，每行格式为 uid(Name) \t groupID  
      //  BufferedWriter bufWrite = new BufferedWriter(new FileWriter(new File("./uidOfgrp.txt")));  
        HashMap<String, Integer> clusterIds;  
        clusterIds = new HashMap<String, Integer>();  
        //IntWritable key = new IntWritable();  
        WeightedPropertyVectorWritable  wvalue = new WeightedPropertyVectorWritable ();  
        while (reader.next(key, wvalue)) {  
            NamedVector vector = (NamedVector) wvalue.getVector();  
           //得到Vector的Name标识  
            String vectorName = vector.getName();  
           // bufWrite.write(vectorName + "\t" + key.toString() + "\n");  
            System.out.println(vectorName + "\t" + key.toString());
           //更新每个group的大小  
            if (clusterIds.containsKey(key.toString())) {  
                clusterIds.put(key.toString(), clusterIds.get(key.toString()) + 1);  
            } else  
                clusterIds.put(key.toString(), 1);  
        }  
        //bufWrite.flush();  
        reader.close();  
        //将每个group的大小，写入grpSize文件中  
      //  bufWrite = new BufferedWriter(new FileWriter(new File("./grpSize.txt")));  
        Set<String> keys = clusterIds.keySet();  
        for (String kk : keys) {  
            //bw.write(k + " " + clusterIds.get(k) + "\n"); 
        	System.out.println(kk + " " + clusterIds.get(kk));
        }  
     //   bufWrite.flush();  
      //  bufWrite.close();  
	}
}
