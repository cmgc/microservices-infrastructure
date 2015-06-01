# Kafka on Mesos Guide
Short guide about kafka-mesos and kafka usage at MI cluster

## kafka-mesos.sh

Kafka-mesos.sh utility is built to control kafka brokers/server on top of mesos.

### Typical operation

Login into dev machine (ssh) 

#### Start kafka brokers

Start with creating/provisioning brokers on top of mesos

      $ ./kafka-mesos.sh add 0..2 --heap 1024 --mem 2048

      Brokers added
      
      brokers:
        id: 0
        active: false
        state: stopped
        resources: cpus:1.00, mem:2048, heap:1024
        failover: delay:10s, max-delay:60s
      
        id: 1
        active: false
        state: stopped
        resources: cpus:1.00, mem:2048, heap:1024
        failover: delay:10s, max-delay:60s
      
        id: 2
        active: false
        state: stopped
        resources: cpus:1.00, mem:2048, heap:1024
        failover: delay:10s, max-delay:60s

Now you are able to start a specific broker:

       $ ./kafka-mesos.sh start 0
       Broker 0 started

       $ ./kafka-mesos.sh start 1
       Broker 1 started

       $ ./kafka-mesos.sh start 2
       Broker 2 started


#### Remove brokers 

      $ ./kafka-mesos.sh help remove
      Remove broker
      Usage: remove <id-expr> [options]
      
      Generic Options
      Option  Description
      ------  -----------
      --api   Api url. Example: http://master:7000
      
      id-expr examples:
        0      - broker 0
        0,1    - brokers 0,1
        0..2   - brokers 0,1,2
        0,1..2 - brokers 0,1,2
        *      - any broker

#### Review current status

      $ ./kafka-mesos.sh status
      Cluster status received
      
      cluster:
        brokers:
          id: 0
          active: true
          state: running
          resources: cpus:1.00, mem:128, heap:128
          failover: delay:10s, max-delay:60s
          task:
            id: broker-0-d2d94520-2f3e-4779-b276-771b4843043c
            running: true
            endpoint: 172.16.25.62:31000
            attributes: rack=r1
      
#### Use help

        $ ./kafka-mesos.sh help add
        Add broker
        Usage: add <id-expr> [options]
        
        Option                Description
        ------                -----------
        --constraints         constraints (hostname=like:master,rack=like:1.*). See below.
        --cpus <Double>       cpu amount (0.5, 1, 2)
        --failover-delay      failover delay (10s, 5m, 3h)
        --failover-max-delay  max failover delay. See failoverDelay.
        --failover-max-tries  max failover tries. Default - none
        --heap <Long>         heap amount in Mb
        --mem <Long>          mem amount in Mb
        --options             kafka options or file. Examples:
                               log.dirs=/tmp/kafka/$id,num.io.threads=16
                               file:server.properties
        
        Generic Options
        Option  Description
        ------  -----------
        --api   Api url. Example: http://master:7000
        
        id-expr examples:
          0      - broker 0
          0,1    - brokers 0,1
          0..2   - brokers 0,1,2
          0,1..2 - brokers 0,1,2
          *      - any broker
        
        constraint examples:
          like:master     - value equals 'master'
          unlike:master   - value not equals 'master'
          like:slave.*    - value starts with 'slave'
          unique          - all values are unique
          cluster         - all values are the same
          cluster:master  - value equals 'master'
          groupBy         - all values are the same
          groupBy:3       - all values are within 3 different groups

## Basic kafka usage

Make SSH connection to any Mesos follower (see your inventory file) using "centos" user. 

1.  Create a topic named "test" with a single partition and one replica:

        $ kafka-topics.sh --create --zookeeper zookeeper.service.consul:2181 --replication-factor 1 --partitions 1 --topic test

    You should obtain:

        Created topic "test".

2. Check that new topic is created by running list topic command:

        $ kafka-topics.sh --list --zookeeper zookeeper.service.consul:2181

    You should obtain:

        test

3. Run the producer and then type a few messages into the console. Instead of `<endpoint>` use any kafka broker endpoint received from output of `./kafka-mesos.sh status` command. It would be something like `host-04:4001` or similar.

        $ kafka-console-producer.sh --broker-list <endpoint> --topic test
        message one
        message two

    Run the consumer that will dump out messages to standard output.

        kafka-console-consumer.sh --zookeeper zookeeper.service.consul:2181 --topic test --from-beginning

    You should obtain:

        message one
        message two


_Note: If you have each of the above commands (producer and consumer) running in a different terminal then you should be able to type messages into the producer terminal and observe them appear in the consumer terminal._
