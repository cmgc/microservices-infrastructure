Create Mesos Cluster
====================

Purpose
-------

Create Mesos Cluster in one datacenter from scratch using microservices-infrastructure project.

Pre-requisites
--------------

All steps from `Provision Open Stack Cluster <provision_open_stack_cluster.rst>`_ have been done.

Step-by-step Guide
------------------

1. Ping all instances to ensure they are reachable via SSH::

        ansible all -i inventory/<your inventory file> -m ping

   Note: If it fails, you might need to remove old records from `~/.ssh/known_hosts`.

2. Run::

        ./security-setup --enable=false

   The script will ask you for admin password for all the UIs (Mesos, Marathon and Consul).

3. Add additional users if needed:

   Go to `inventory/group_vars/all` folder and edit `users.yml`.
   Add all the needed users and their public keys.

4. If you want to use a particular version of Spark ("1.3.0" is used by default),
   then edit `roles/spark/defaults/main.yml` and set::

        spark_default_version: "<version number>"

   For example::

        spark_default_version: "1.3.1"

   If later you want to temporarily change the Spark version, run the command below
   (on the client machine)::

        source /usr/local/share/spark/<correct spark folder>/conf/spark-env.sh

   For example::

        source /usr/local/share/spark/spark-1.3.1-bin-hadoop2.6/conf/spark-env.sh

   It will change the Spark version only for the current user session.

   If you want to permanently change the Spark version, then copy a correct
   `spark-env.sh` to `/etc/profile.d`.

5. Run::

        ansible-playbook -i inventory/<your inventory file> site.yml -e @security.yml

6. Verify all the services (use "admin" as the user name and the password you set for
   `security-setup`):

   *Mesos:*

   Open *https://<any mesos_leader>:5050*
   Open *https://<any mesos_leader>:5050/state.json*
   Open *https://<any mesos_leader>:5050/stats.json*

   *Consul:*

   Open *https://<any consul_server>:8500* and make sure that all services are passing

   *Marathon:*

   Open *https://<any marathon_server>:8080*.  Click "+ New App" and create some
   test application (for example, id: "sleep" and command: "sleep 3600").

   Note: If in Firefox you encounter "Secure Connection Failed" error, please try
   another browser (for example, Google Chrome).

7. Verify HDFS:

   Make SSH connection to any Mesos follower (see your inventory file) using
   "centos" user and run::

        hdfs dfs -ls /

   You should obtain something like::

        drwxr-xr-x   - hdfs supergroup          0 2015-04-24 14:30 /apps
        drwxrwxrwx   - hdfs supergroup          0 2015-04-24 14:37 /tmp
        drwxr-xr-x   - hdfs supergroup          0 2015-04-24 14:30 /user

   Put a file on HDFS::

        hdfs dfs -put <file>
        hdfs dfs -ls

   Make sure your file is there.

8. Verify Spark:

   Make SSH connection to any Mesos follower (see your inventory file) using
   "centos" user and run::

        spark-shell

   Spark shell should start with no errors::

        scala>

   Run the following commands::

        val data = 1 to 10000
        val distData = sc.parallelize(data)
        val filteredData = distData.filter(_< 10)
        filteredData.collect()

   You should obtain::

        res0: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9)

   Make sure that `/tmp/test` doesn't exist on HDFS yet. Run::

        filteredData.saveAsTextFile("hdfs:///tmp/test")

   The command should finish without errors.  Exit Spark shell::

        exit

   Run::

        hdfs dfs -cat /tmp/test/part-00000

   You should obtain::

        1
        2
        3
        4
        5
        6
        7
        8
        9

   Run::

        run-example SparkPi

   You should obtain something like::

        Pi is roughly 3.14336

9. Verify Kafka-mesos utility:

   Make SSH connection to any Mesos follower (see your inventory file)
   using "centos" user and run::

        cd /usr/local/share/kafka-mesos

   After that run::

        ./kafka-mesos.sh status

   You should obtain something like::

        Cluster status received
        
        cluster:
          brokers:
            id: 0
            active: true
            state: running
            resources: cpus:0.50, mem:512, heap:256
            failover: delay:10s, max-delay:60s
            task:
              id: broker-0-67e702ad-c719-493e-8e19-95ecb8151dec
              state: running
              endpoint: aomelian-ci-host-04:4001
              attributes: node_id=aomelian-ci-host-04
        
        <next output is omitted>

   Note: amount of Kafka brokers and their mem/heap values depends on configuration
   file `roles/kafka/defaults/main.yml` inside your project directory.

10. Verify basic Kafka functionality:

    Make SSH connection to any Mesos follower (see your inventory file) using "centos" user. 
    Create a topic named "test" with a single partition and one replica::

        kafka-topics.sh --create --zookeeper zookeeper.service.consul:2181 --replication-factor 1 --partitions 1 --topic test

    You should obtain::

        Created topic "test".

    Check that new topic is created by running list topic command::

        kafka-topics.sh --list --zookeeper zookeeper.service.consul:2181

    You should obtain::

        test

    Run the producer and then type a few messages into the console.  Instead of
    `<endpoint>` use any Kafka broker endpoint received from step 8.  It would be
    something like `host-04:4001` or similar::

        kafka-console-producer.sh --broker-list <endpoint> --topic test
        message one
        message two

    Run the consumer that will dump out messages to standard output::

        kafka-console-consumer.sh --zookeeper zookeeper.service.consul:2181 --topic test --from-beginning

    You should obtain::

        message one
        message two

    Note: If you have each of the above commands (producer and consumer) running
    in a different terminal then you should be able to type messages into the
    producer terminal and see them appear in the consumer terminal.
