Kafka Mesos
===========

`Apache Kafka <https://kafka.apache.org>`_ is a publish-subscribe messaging rethought as a distributed commit log.

Variables
---------

- `kafka_mesos_install_dir` define folder for kafka-mesos installation. Default: `/usr/local/share/kafka-mesos`
- `kafka_binary_url`: define URL for kafka binary installation. Default: `https://archive.apache.org/dist/kafka/`
- `kafka_version`: specify version of kafka that will be used. Default: `0.8.2.1`
- `kafka_scala_version`: version of scala. Default: `2.10`
- `kafka_mesos_repo`: mesos-kafka repo URL. Default: `https://github.com/mesos/kafka`
- `mesos_lib`: Specify mesos library location. Default: `/usr/local/lib/libmesos.so`
- `zookeeper_master`: Specify FQDN for zookeeper master. Default for MI project is `zookeeper.service.consul`
- `marathon`: Specify FQDN for marathon services. Default for MI project is `marathon.service.consul`
- `kafka_scheduler_hostname`: hostname of kafka mesos scheduler. Default: `kafka-mesos-scheduler.service.consul`
- `kafka_brokers`: Define number of brokers that will be used in your cluster. Default: `3`
- `kafka_broker_memory`: Specify Java memory setting for broker. Default: `512`
- `kafka_broker_heap`: Specify Java heap for broker. Default: `256`
- `debug_enabled`: enable or disable debug mode for kafka-mesos. Default: `false`

Example Playbook
----------------

.. code-block:: yaml+jinja

    ---
    - hosts: mesos_followers
      gather_facts: no
      roles:
        - kafka-mesos
