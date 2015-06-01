Provision Open Stack Cluster
============================

Purpose
-------

Provision OpenStack cluster in one datacenter from scratch using
microservices-infrastructure project.

Pre-requisites
--------------

1. Access to the project in Openstack Horizon Portal.

2. Linux environment with sudo access.

Step-by-step Guide
------------------

1. Clone microservices-infrastructure project from GitHub.  At the moment you can
   choose between various branches, but for general purposes it is suggested to use
   either "qa/features-master-integration" or "features-master".

   To clone the master branch::

        git clone https://github.com/CiscoCloud/microservices-infrastructure.git <folder>

   To clone another branch::

        git clone https://github.com/CiscoCloud/microservices-infrastructure.git -b '<branch name>' <folder>

   It will create <folder> folder and put all the files there.

2. Review `requirements.txt` and make sure that all the needed dependencies or
   their later versions are installed.  Try::

        pip show <name>

   Install missing dependencies if needed.  Try::

        sudo pip install <name>

   or if you need to upgrade an older version::

        sudo pip install --upgrade <name>

3. Get OpenStack tenant settings:

   Login into Openstack Horizon Portal, select Access & Security, select API Access tab
   and then click "Download OpenStack RC file".  Download the file and copy it to your
   environment.  Export all the environment variables from the file::

        source <your file>

   It will prompt you for your OpenStack password.

4. Get your network id:

   Display the list of all available OpenStack networks::

        neutron net-list

   Find a network, which is accessible from your environment (for example, "public-direct-600").

5. Create a new security group called "microservice"::

        nova secgroup-create microservice "microservices-infrastructure"
        nova secgroup-add-rule microservice icmp -1 -1 0.0.0.0/0
        nova secgroup-add-rule microservice tcp 22 22 0.0.0.0/0
        nova secgroup-add-rule microservice tcp 80 80 0.0.0.0/0
        nova secgroup-add-rule microservice tcp 5050 5050 0.0.0.0/0
        nova secgroup-add-rule microservice tcp 8080 8080 0.0.0.0/0
        nova secgroup-add-rule microservice tcp 8500 8500 0.0.0.0/0
        nova secgroup-add-group-rule microservice microservice tcp 1 65535

6. Save OpenStack settings in a datacenter file:

   Go to `inventory/group_vars` folder and edit either `dc1` or `dc2` (at the moment
   it's not possible to use files with your own names).  Set "os_auth_url",
   "os_tenant_name" and "os_tenant_id" using the values from OpenStack RC-file that
   you got in step 3 (see its content).  Set "os_net_id" to the "id" of the chosen
   network (see step 4).  Set "security_group" to "microservice".

7. Create inventory file:

   Go to `inventory` folder and either edit existing `1-datacenter` or `2-datacenter`
   or create a new file using one of them as a template.  Update the number of hosts
   and their hostnames if needed.  Update datacenters if needed.

8. Update the flavor of the instances if needed:

   Go to `inventory/group_vars/all` folder and edit `all.yml`.  Update
   "os_flavor_ram" and "os_flavor_include" if needed (it is suggested to set at least
   "8192" and "GP2-Large").  Make sure you have selected an existing
   "os_flavor_ram/os_flavor_include" combination.

9. Add your SSH key to OpenStack:

   Make sure that `${HOME}/.ssh/id_rsa.pub` file exists.  You can either generate
   a new key or use some external one.  After that run::

        ansible-playbook -i inventory/<your inventory file> openstack/provision-nova-key.yml

   Note: When you add a keypair with Nova, it's being added for all tenants in the
   current zone.  That is why if you see that the default "ansible_key" is already
   present in the system, don't remove or alter it.  Otherwise, someone will lose
   access to his or her environment. Instead, it has been agreed for our team to use
   the shared gluon private key (and the corresponding public key) for all deployments.
   Here are links to the keys::

        http://gitlab.cisco.com/ccs-bdaas-projects/ccs-bdaas/blob/master/CCS-GLUON/id_rsa_gluonmi
        http://gitlab.cisco.com/ccs-bdaas-projects/ccs-bdaas/blob/master/CCS-GLUON/id_rsa_gluonmi.pub

   You need to put them as id_rsa and id_rsa.pub in your $HOME/.ssh directory on the gluon host.

10. Provision hosts::

        ansible-playbook -i inventory/<your inventory file> openstack/provision-hosts.yml
 
    Login into Openstack Horizon Portal, select Instances and verify that all the instances
    have been provisioned.

    If you need to destroy your cluster, run::

        ansible-playbook -i inventory/<your inventory file> openstack/destroy-hosts.yml

    Note: It's most likely that you will need to add IPs of provisioned instances into your
    `/etc/hosts`, otherwise you won't be able to access them.  To do that just copy the content
    of `hosts.merge` (it should be created by `openstack/provision-hosts.yml`) into `/etc/hosts`.
    When you destroy the cluster, don't forget to remove them from `/etc/hosts`.

Demo Environment
----------------

It should be always working and ready for demos::

        CCS-MI-US-INTERNAL-1-CI-1

        host-01 ansible_ssh_host=10.203.30.29
        host-02 ansible_ssh_host=10.203.30.31
        host-03 ansible_ssh_host=10.203.30.37
        host-04 ansible_ssh_host=10.203.30.35
        host-05 ansible_ssh_host=10.203.30.30

Use the gluon private key to ssh to the hosts.
