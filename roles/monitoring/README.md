## collectd

Monitoring role for deploying and managing [collectd](https://collectd.org) service on host operating systems.
Sends collected metrics to user-defined (defaults/main.yml) host, those can be easily analyzed via Logstash.

## User-customizable variables

You can use these variables (defaults/main.yml) to customize your collectd installation.

| var | description | default |
|-----|-------------|---------|
|`logging_host`|host to receive collectd's metrics over the network| {{ ansible_ssh_host }}|
|`logging_host_port`|port to receive collectd's metrics over the network| 25826|
|`mesos_master_host`|host to get mesos master data from|localhost|
|`mesos_master_port`|mesos master http port|15050|
|`mesos_slave_host`|host to get mesos slave data from|localhost|
|`mesos_slave_port`|mesos slave http port|15050|
|`zookeper_hosts`|zookeper hosts to get metrics from|localhost|
