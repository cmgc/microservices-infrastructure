Launch a Spark Job from Outside of the Cluster
==============================================

Purpose
-------

Run a Spark job from a client machine outside of the cluster.

Pre-requisites
--------------

All steps from `Create Mesos Cluster <create_mesos_cluster.rst>`_ have been done.

Step-by-step Guide
------------------

1. If the client machine is in the same datacenter, tenant and security group as the cluster,
   you don't need to do anything.  If it's not, then open two additional ports for the cluster's
   security group::

        nova secgroup-add-rule microservice tcp 2181 2181 0.0.0.0/0
        nova secgroup-add-rule microservice tcp 15050 15050 0.0.0.0/0

2. Run `dev.yml` playbook to install on the client machine all the default developer's software::

        ansible-playbook -i "<client machine's hostname>," -u centos -e "hdfs_namenode_host=<hostname of HDFS name node> mesos_leader_host=<hostname of any Mesos leader>" dev.yml

   Please note a comma after the client machine's hostname.

   If later you want to temporarily change the Spark version, run the command below (on the client machine)::

        source /usr/local/share/spark/<correct spark folder>/conf/spark-env.sh

   For example::

        source /usr/local/share/spark/spark-1.3.1-bin-hadoop2.6/conf/spark-env.sh

   It will change the Spark version only for the current user session.

   If you want to permanently change the Spark version, then copy a correct `spark-env.sh` to `/etc/profile.d`.

3. Make sure that FQDN of the client machine (not only its IP or hostname like "host-01") is
   accessible from each Mesos follower of the cluster.  If it's not, then you have to manually add its
   FQDN to `/etc/hosts` on each Mesos follower.

4. Certain ports must be opened on the client machine.  If the client machine is in the same datacenter,
   tenant and security group as the cluster, you don't need to do anything.  If it's not, then check
   whether your local ports are opened or not.  You can find the range of your local IPs by running::

        sysctl net.ipv4.ip_local_port_range

   By default the range is from 32768 to 61000.  If the range is not opened, then you have two options:

   Option 1. If you don't mind opening the whole range of ports OR you plan to run several Spark jobs
   simultaneously, then just open the whole range.  How to do that depends on where the client machine is.
   If it's on OpenStack, then you can open them like::

        nova secgroup-add-rule microservice tcp 32768 61000 0.0.0.0/0

   Make sure to open the ports in the client machine's tenant, not in the cluster's tenant.

   Option 2. If you don't want to open the whole range of ports AND you don't plan to run several Spark jobs
   simultaneously, then do the following:

   Choose four ports from the available range.

   Go to your actual Spark folder on the client machine.  Edit `spark-defaults.conf` and add the following lines::

        spark.driver.port                  <port 1>
        spark.replClassServer.port         <port 2>
        spark.blockManager.port            <port 3>

   Edit `spark-env.sh` and add the following line::

        export LIBPROCESS_PORT=<port 4>

   If you installed Spark client using `dev.yml`, then you also have to copy `spark-env.sh` to `/etc/profile.d`.

   Open all four ports on the client machine.  How to do that depends on where the client machine is.
   If it's on OpenStack, then you can open them like::

        nova secgroup-add-rule microservice tcp <port 1> <port 1> 0.0.0.0/0
        nova secgroup-add-rule microservice tcp <port 2> <port 2> 0.0.0.0/0
        nova secgroup-add-rule microservice tcp <port 3> <port 3> 0.0.0.0/0
        nova secgroup-add-rule microservice tcp <port 4> <port 4> 0.0.0.0/0

5. Verify HDFS.

   Make SSH connection to the client machine and run::

        hdfs dfs -ls /

   You should obtain something like::

        drwxr-xr-x   - hdfs supergroup          0 2015-04-24 14:30 /apps
        drwxrwxrwx   - hdfs supergroup          0 2015-04-24 14:37 /tmp
        drwxr-xr-x   - hdfs supergroup          0 2015-04-24 14:30 /user

   Put a file on HDFS::

        hdfs dfs -put <file>
        hdfs dfs -ls

   Make sure your file is there.

6. Verify Spark.

   Run::

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

        run-example SparkPi

   You should obtain something like::

        Pi is roughly 3.14336
