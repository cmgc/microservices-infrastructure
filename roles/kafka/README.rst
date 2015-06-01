Kafka
=====

`Apache Kafka <https://kafka.apache.org>`_ is a publish-subscribe messaging rethought as a distributed commit log.

Variables
---------

- `kafka_install_dir`: define folder for kafka installation. Default: `/usr/local/share/kafka`
- `kafka_binary_url`: define URL for kafka binary installation. Default: `https://archive.apache.org/dist/kafka/`
- `kafka_version`: specify version of kafka that will be used. Default: `0.8.2.1`
- `kafka_scala_version`: version of scala. Default: `2.10`

Example Playbook
----------------

.. code-block:: yaml+jinja

    ---
    - hosts: mesos_followers
      gather_facts: no
      roles:
        - kafka
