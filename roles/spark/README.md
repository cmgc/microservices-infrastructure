# Spark

[Apache Spark](https://spark.apache.org/) is a fast and general engine for big
data processing, with built-in modules for streaming, SQL, machine learning and
graph processing.

## Variables

- `hadoop_version` - Hadoop version Spark binary is built for (default: `2.6`).
- `spark_version` - Spark version to be installed (default: `1.3.1`).
- `spark_user` - Linux user to run Spark jobs (default: `centos`).
- `spark_install_dir` - Local directory where to put Spark binary and Spark
  client (default: `/usr/local/share/spark`).
- `spark_hdfs_dir` - HDFS directory where to put Spark binary
  (default: `/apps/spark`) [not used in the current version].
- `spark_mesos_lib` - Path to `libmesos.so` (default:
  `/usr/local/lib/libmesos.so`).
- `zookeeper_master` - Hostname of Zookeeper master (default:
  `zookeeper.service.consul`).

## Example Playbook

    ---
    - hosts: mesos_followers
      gather_facts: no
      roles:
        - spark
