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
import org.apache.hadoop.fs.FileStatus;

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
	// hdfs://rsync.master004.mars.sjs.ted:8020
	private static final String HDFS = "hdfs://10.129.250.52:9000";
	public static final double[][] points = { { 1, 1 }, { 2, 1 }, { 1, 2 }, { 2, 2 }, { 3, 3 }, { 8, 8 }, { 9, 8 },
			{ 8, 9 }, { 9, 9 } };

	public static List<Path> ShowHDFSPartFiles(FileSystem hdfs, Path path) {
		List<Path> path_list = new ArrayList<Path>();
		try {
			if (hdfs == null || path == null) {
				return path_list;
			}

			// 获取文件列表
			FileStatus[] files = hdfs.listStatus(path);
			// 展示文件信息
			for (int i = 0; i < files.length; i++) {
				try {
					if (files[i].isFile()) {
						Path part = files[i].getPath();
						if (part.getName().startsWith("part-")) {
							path_list.add(files[i].getPath());
						}
						/*
						 * System.out.println("   " + files[i].getPath() + ", length:" +
						 * files[i].getLen() + ", owner:" + files[i].getOwner());
						 */
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return path_list;
	}

	public static Path GetClusterFinalHdfsPath(FileSystem hdfs, Path path) {
		Path path_final = null;
		try {
			if (hdfs == null || path == null) {
				return path_final;
			}

			// 获取文件列表
			FileStatus[] files = hdfs.listStatus(path);
			// 展示文件信息
			for (int i = 0; i < files.length; i++) {
				try {
					if (files[i].isDirectory()) {
						Path dir = files[i].getPath();
						if (dir.getName().endsWith(Cluster.FINAL_ITERATION_SUFFIX)) {
							path_final = files[i].getPath();
						}
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return path_final;
	}
	
	// public static void writePointsToFile(List<Vector> points,String
	// fileName,FileSystem fs, Configuration conf) throws IOException {
	@SuppressWarnings("deprecation")
	public static void writePointsToFile(List<NamedVector> points, String fileName, FileSystem fs, Configuration conf)
			throws IOException {
		Path path = new Path(fileName);
		SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf, path, Text.class, VectorWritable.class);
		// long recNum = 0;
		VectorWritable vec = new VectorWritable();
		// for (Vector point : points) {
		for (NamedVector point : points) {
			vec.set(point);
			// writer.append(new LongWritable(recNum++), vec);
			writer.append(new Text(point.getName()), vec);
		}
		writer.close();
	}
 
	// public static List<Vector> getPoints(double[][] raw) {
	public static List<NamedVector> getPoints(double[][] raw, String name) {
		
		// List<Vector> points = new ArrayList<Vector>();
		List<NamedVector> points = new ArrayList<NamedVector>();
		for (int i = 0; i < raw.length; i++) {
			double[] fr = raw[i];
			Vector vec = new RandomAccessSparseVector(fr.length);
			vec.assign(fr);
			NamedVector vecName;
			vecName = new NamedVector(vec, name + i);
			points.add(vecName);
		}
		return points;
	}

	@SuppressWarnings("deprecation")
	public static void main(String args[]) throws Exception {
		// System.setProperty("HADOOP_USER_NAME", "wangdan209498");
		
		String input = "/clustering/testdata/points/";
		String output = "/clustering/output/";
		String initPath = "/clustering/testdata/clusters/";
		
		// getPoints(points);//根据初始点坐标数组构建成为聚类算法能够处理的vector的list集合格式
		List<NamedVector> vectorsA = getPoints(points, "dataA");// 根据初始点坐标数组构建成为聚类算法能够处理的vector的list集合格式
		List<NamedVector> vectorsB = getPoints(points, "dataB");
		Configuration conf = new Configuration();
		FileSystem fs = FileSystem.get(new URI("hdfs://10.129.250.52:9000/"), conf, "/");
		
		writePointsToFile(vectorsA, input + "file1", fs, conf);// 将点的集合写到hdfs上的数据文件中名称为file1
		writePointsToFile(vectorsB,  input + "file2", fs, conf);// 将点的集合写到hdfs上的数据文件中名称为file1
		
		Path path = new Path(initPath + "/part-00000");// 初始化点
		@SuppressWarnings("deprecation")
		SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf, path, Text.class, Kluster.class);

		// 初始化中心点k=2
		int k = 2;
		for (int i = 0; i < 5; i++) {
			Vector vec = vectorsA.get(i%3);
			// cluster--{"r":[],"c":[1.0,1.0],"n":0,"identifier":"CL-0"}
			Kluster cluster = new Kluster(vec, i, new EuclideanDistanceMeasure());
			writer.append(new Text(cluster.getIdentifier()), cluster);
		}
		writer.close();
		
		Path hdfsInput = new Path(HDFS + input);
		Path hdfsInitCluser = new Path(HDFS + initPath);
		Path hdfsOut = new Path(HDFS + output);
		// 运行聚类算法
		KMeansDriver.run(conf, hdfsInput, // 原始输入
				hdfsInitCluser, // 初始中心点集合
				hdfsOut, // 聚类结果
				0.001, 5, true, 0, false);

		////////////////////////////////////////////////////
		// 从HDFS上读取聚类结果
		// @SuppressWarnings("deprecation")
		
		Path final_path = GetClusterFinalHdfsPath(fs, new Path(output));
		System.out.println(final_path);
		SequenceFile.Reader reader = new SequenceFile.Reader(fs, new Path(final_path + "/part-r-00000"), conf);
		IntWritable key = new IntWritable();
		ClusterWritable value = new ClusterWritable();
		while (reader.next(key, value)) {
			System.out.println(value.getValue().toString() + " belongs to cluster " + key.toString());
		}
		reader.close();

		List<Path> outPutPartPaths = ShowHDFSPartFiles(fs, new Path(output + Cluster.CLUSTERED_POINTS_DIR));
		// 将分组信息写到文件uidOfgrp.txt，每行格式为 uid(Name) \t groupID
		// BufferedWriter bufWrite = new BufferedWriter(new FileWriter(new
		// File("./uidOfgrp.txt")));
		HashMap<String, Integer> clusterIds;
		clusterIds = new HashMap<String, Integer>();
		for (Path partPath : outPutPartPaths) {
			reader = new SequenceFile.Reader(fs, partPath, conf);
			// IntWritable key = new IntWritable();
			WeightedPropertyVectorWritable wvalue = new WeightedPropertyVectorWritable();
			while (reader.next(key, wvalue)) {
				NamedVector vector = (NamedVector) wvalue.getVector();
				// 得到Vector的Name标识
				String vectorName = vector.getName();
				// bufWrite.write(vectorName + "\t" + key.toString() + "\n");
				System.out.println(vectorName + "\t" + key.toString());
				// 更新每个group的大小
				if (clusterIds.containsKey(key.toString())) {
					clusterIds.put(key.toString(), clusterIds.get(key.toString()) + 1);
				} else
					clusterIds.put(key.toString(), 1);
			}
			// bufWrite.flush();
			reader.close();
		}
		// 将每个group的大小，写入grpSize文件中
		// bufWrite = new BufferedWriter(new FileWriter(new File("./grpSize.txt")));
		Set<String> keys = clusterIds.keySet();
		for (String label : keys) {
			// bw.write(k + " " + clusterIds.get(k) + "\n");
			System.out.println("label\t" + label + "\tcount\t" + clusterIds.get(label));
		}
		// bufWrite.flush();
		// bufWrite.close();
	}
}
