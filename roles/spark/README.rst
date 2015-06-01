Spark
=====

`Apache Spark <https://spark.apache.org/>`_ is a fast and general engine for big
data processing, with built-in modules for streaming, SQL, machine learning and
graph processing.

Variables
---------

- `spark_versions` - Spark versions to be installed (default:
  `["1.2.1", "1.2.2", "1.3.0", "1.3.1"]`).
- `spark_default_version` - Default Spark version to use (default: `1.3.0`).
- `spark_install_dir` - Local directory where to put Spark binary and Spark
  client (default: `/usr/local/share/spark`).
- `spark_mesos_lib` - Path to `libmesos.so` (default:
  `/usr/local/lib/libmesos.so`).
- `zookeeper_master` - Hostname of Zookeeper master (default:
  `zookeeper.service.consul`).
- `spark_log4j_host` - Hostname for logstash server (default: `localhost`).
- `spark_log4j_port` - Port for logstash server (default: `4560`).

Example Playbook
----------------

.. code-block:: yaml+jinja

    ---
    - hosts: mesos_followers
      gather_facts: no
      roles:
        - spark
