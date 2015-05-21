# Spark

[Apache Kafka](https://kafka.apache.org) is publish-subscribe messaging rethought as a distributed commit log

## Variables

- `kafka_install_dir`: define folder for kafka installation. Default `/usr/local/share/kafka`
- `kafka_mesos_install_dir` define folder for kafka-mesos installation. Default `/usr/local/share/kafka-mesos`
- `kafka_binary_url`: define URL for kafka binary installation. Default: https://archive.apache.org/dist/kafka/0.8.1.1/
- `kafka_archive`: kafka archive name. Default:  kafka_2.9.2-0.8.1.1.tgz
- `kafka_mesos_repo`: mesos-kafka repo URL. Default: https://github.com/mesos/kafka
- `mesos_lib`: Specify mesos library location. Default: `/usr/local/lib/libmesos.so`
- `zookeeper_master`: Specify FQDN for zookeeper master. Default for MI project is `zookeeper.service.consul`
- `marathon`: Specify FQDN for marathon services. Default for MI project is `marathon.service.consul`
- `kafka_scheduler_hostname`: hostname of kafka mesos scheduler. Default: `kafka-mesos-scheduler.service.consul`
- `kafka_brokers`: Define number of brokers that will be used in your cluster. Default: 3
- `kafka_broker_memory`: Specify Java memory setting for broker. Default: 2048
- `kafka_broker_heap`: Specify Java heap for broker. Default: 1024 
- `debug_enabled`: enable or dissable debug mode for kafka-mesos. Default: false

## Example Playbook

    ---
    - hosts: mesos_followers
      gather_facts: no
      roles:
        - kafka
