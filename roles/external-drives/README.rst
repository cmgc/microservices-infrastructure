External Drives
===============

Create and attach an external drive and re-configure HDFS to use it.

Variables
---------

- `storage_device` - Storage device (default: `vdb`).
- `storage_size` - Storage size in GB (default: `1024`).

Example Playbook
----------------

.. code-block:: yaml+jinja

    ---
    - hosts: data_nodes
      gather_facts: no
      roles:
        - external-drives
