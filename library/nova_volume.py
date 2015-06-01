#!/usr/bin/python
#coding: utf-8 -*-

# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import operator
import os

try:
    from novaclient.v1_1 import client as nova_client
    from novaclient.v1_1 import floating_ips
    from novaclient.v1_1.client import Client
    from novaclient import exceptions
    from novaclient import utils
    from keystoneclient.auth.identity import v2
    from keystoneclient import session
    import time
except ImportError:
    print("failed=True msg='novaclient is required for this module'")

def _detach_block_device(module, nova, volume):
    nova.client.service_type = "compute"
    if volume.attachments:
        for attachment in volume.attachments:
            try:
                nova.volumes.delete_server_volume(attachment['server_id'],attachment['id'])
            except Exception, e:
                module.fail_json( msg = "Error while deleting volume: %s" % e.message)
                pass

    expire = time.time() + int(module.params['wait_for'])
    nova.client.service_type = "volume"
    while time.time() < expire:
        new_volume = None
        try:
            new_volume = nova.volumes.get(volume.id)
        except Exception, e:
            module.fail_json( msg = "Error in getting info from volume: %s" % e.message)
        if new_volume.status == 'available':
            break
        time.sleep(1)
    return True

def _delete_block_device(module, nova):
    nova.client.service_type = "volume"
    try:
        volumes = nova.volumes.list(True, {'display_name': module.params['name']})
    except Exception, e:
        pass

    if volumes:
        volume = volumes[0]
    else:
       return

    if volume.status == 'in-use':
        _detach_block_device(module, nova, volume)


    nova.volumes.delete(volume)
    module.exit_json(changed = True, result = "deleted")


def _create_block_device(module, nova):

    nova.client.service_type = "volume"

    new_volume = nova.volumes.create(size=module.params['size'], display_name=module.params['name'])

    if module.params['wait'] == 'yes':
        expire = time.time() + int(module.params['wait_for'])
        while time.time() < expire:
            try:
                new_volume = nova.volumes.get(new_volume.id)
            except Exception, e:
                module.fail_json( msg = "Error in getting info from volume: %s" % e.message)
            if new_volume.status == 'available':
                break
            if new_volume.status == 'error':
                module.fail_json(msg = "Error in creating the volume, please check logs")
            time.sleep(1)
        if new_volume.status != 'available':
           module.fail_json(msg = "Timeout waiting for the volume to come up.. Please check manually")
    if new_volume.status == 'error':
        module.fail_json(msg = "Error in creating the volume.. Please check manually")
    return new_volume


def _attach_block_device(module, nova, server, volume):

    nova.client.service_type = "compute"

    volume = nova.volumes.create_server_volume(server.id, volume.id, module.params['device_name'])

    # cdmitri: Need to switch back to volume in order to get status
    nova.client.service_type = "volume"

    # cdmitri: use the same setting for volume waits as for server
    if module.params['wait'] == 'yes':
        expire = time.time() + int(module.params['wait_for'])
        while time.time() < expire:
            try:
                volume = nova.volumes.get(volume.id)
            except Exception, e:
                module.fail_json( msg = "Error in getting info from attached volume: %s" % e.message)
            if volume.status == 'in-use':
                break
            if volume.status == 'error':
                module.fail_json(msg = "Error in attaching the volume, please check logs")
            time.sleep(1)
        if volume.status != 'in-use':
           module.fail_json(msg = "Timeout waiting for the volume to come up.. Please check manually")
    if volume.status == 'error':
        module.fail_json(msg = "Error in attaching the volume.. Please check manually")
    return volume


def _create_volume(module, nova):

    nova.client.service_type = "volume"
    try:
        volumes = nova.volumes.list(True, {'display_name': module.params['name']})
    except Exception, e:
        pass

    if volumes:
        volume = volumes[0]
    else:
        volume = _create_block_device(module, nova)

    nova.client.service_type = "compute"
    server = None
    if module.params['server']:
        try:
            servers = nova.servers.list(True, {'name': module.params['server']})
            if servers:
                # the {'name': module.params['name']} will also return servers
                # with names that partially match the server name, so we have to
                # strictly filter here
                servers = [x for x in servers if x.name == module.params['server']]
            if servers:
               server = servers[0]
            else:
                module.fail_json(msg = "Server %s could not be found" % module.params['server'] )
        except Exception, e:
            module.fail_json(msg = "Error in getting the server list: %s" % e.message)
        #if volume.
        if volume.status == 'in-use':
            attached_to = volume.attachments[0]['server_id']
            if attached_to != server.id:
                module.fail_json(msg = "Volume is already  attached to another server with id %s" % attached_to )
            else:
                module.exit_json(changed = False, id = volume.id, status = volume.status, info = volume._info)
        else:
            attached = _attach_block_device(module, nova, server, volume)

    module.exit_json(changed = True, id = volume.id, status = volume.status, info = volume._info)


def _get_volume_state(module, nova):
    volume = None

    try:
        nova.client.service_type = "volume"
        volumes = nova.volumes.list(True, {'display_name': module.params['name']})
    except Exception, e:
        module.fail_json(msg = "Error in getting the volume list: %s" % e.message)

    if volumes:
        if len(volumes) > 1:
            module.fail_json(msg = "Theres are already %d volumes exist with display name '%s'" % (len(volumes), module.params['name']))

    if volumes and module.params['state'] == 'absent':
        return True

    if module.params['state'] == 'absent':
        module.exit_json(changed = False, result = "not present")


    return True


def main():
    argument_spec = openstack_argument_spec()
    argument_spec.update(dict(
        name                            = dict(required=True),
        server                          = dict(default=None),
        device_name                     = dict(default=None),
        size                            = dict(default=None),
        wait                            = dict(default='yes', choices=['yes', 'no']),
        wait_for                        = dict(default=180),
        state                           = dict(default='present', choices=['absent', 'present']),
    ))
    module = AnsibleModule(
        argument_spec=argument_spec
    )

    auth = v2.Password(auth_url=module.params['auth_url'],
                       username=module.params['login_username'],
                       password=module.params['login_password'],
                       tenant_name=module.params['login_tenant_name'])

    sess = session.Session(auth=auth)

    try:
        nova = Client(session=sess,region_name=module.params['region_name'])
    except exceptions.Unauthorized, e:
        module.fail_json(msg = "Invalid OpenStack Nova credentials.: %s" % e.message)
    except exceptions.AuthorizationFailure, e:
        module.fail_json(msg = "Unable to authorize user: %s" % e.message)

    if module.params['state'] == 'present':
        if not module.params['size']:
            module.fail_json( msg = "Parameter 'size' is required if state == 'present'")
        else:
            _get_volume_state(module, nova)
            _create_volume(module, nova)
    if module.params['state'] == 'absent':
        _get_volume_state(module, nova)
        _delete_block_device(module, nova)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
main()
