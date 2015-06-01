Dev
===

Install all the needed development software on the client machine.

Run::

    ansible-playbook -i "<client machine's hostname>," -u centos -e "hdfs_namenode_host=<hostname of HDFS name node> mesos_leader_host=<hostname of any Mesos leader>" dev.yml

Variables
---------

N/A

Example Playbook
----------------

.. code-block:: yaml+jinja

    ---
    - hosts: all
      gather_facts: no
      roles:
        - dev
        - {role: hdfs-standalone, hdfs_namenode: false, hdfs_datanode: false}
        - spark

    - hosts: all
      gather_facts: yes
      roles:
        - kafka
