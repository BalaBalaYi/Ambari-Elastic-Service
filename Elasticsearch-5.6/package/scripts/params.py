# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Elasticsearch Params configurations
"""

from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import status_params
import os

config = Script.get_config()

es_home = '/etc/elasticsearch/'
es_bin = '/opt/elasticsearch/bin/'

java64_home = config['hostLevelParams']['java_home']

hostname = config['hostname']


# env
es_user = config['configurations']['elasticsearch-env']['elasticsearch_user']
es_group = config['configurations']['elasticsearch-env']['elasticsearch_group']

es_base_dir = config['configurations']['elasticsearch-env']['elasticsearch_base_dir']
es_conf_dir = config['configurations']['elasticsearch-env']['elasticsearch_conf_dir']
es_log_dir = config['configurations']['elasticsearch-env']['elasticsearch_log_dir']
es_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch_pid_dir']
es_pid_file = format("{es_pid_dir}/elasticsearch.pid")

es_install_log = es_base_dir + '/elasticsearch-install.log'
es_download_url = config['configurations']['elasticsearch-env']['elasticsearch_download_url']


# config
cluster_name = config['configurations']['elasticsearch-config']['cluster_name']
hostname = config['hostname']
node_attr_rack = config['configurations']['elasticsearch-config']['node_attr_rack']
path_data = config['configurations']['elasticsearch-config']['path_data']
path_logs = config['configurations']['elasticsearch-config']['path_logs']

bootstrap_memory_lock = str(config['configurations']['elasticsearch-config']['bootstrap_memory_lock'])

# 'True' -> 'true', 'False' -> 'false'
if bootstrap_memory_lock == 'True':
    bootstrap_memory_lock = 'true'
else:
    bootstrap_memory_lock = 'false'

network_host = config['configurations']['elasticsearch-config']['{network_host']
http_port = config['configurations']['elasticsearch-config']['http_port']

discovery_zen_ping_unicast_hosts = str(config['configurations']['elasticsearch-config']['discovery_zen_ping_unicast_hosts'])

# Need to parse the comma separated hostnames to create the proper string format within the configuration file
# Expects the format ["host1","host2"]
master_node_list = discovery_zen_ping_unicast_hosts.split(',')
discovery_zen_ping_unicast_hosts = '[' +  ','.join('"' + x + '"' for x in master_node_list) + ']'

discovery_zen_minimum_master_nodes = config['configurations']['elasticsearch-config']['discovery_zen_minimum_master_nodes']

gateway_recover_after_nodes = config['configurations']['elasticsearch-config']['gateway_recover_after_nodes']
node_max_local_storage_nodes = config['configurations']['elasticsearch-config']['node_max_local_storage_nodes']

action_destructive_requires_name = str(config['configurations']['elasticsearch-config']['action_destructive_requires_name'])

# 'True' -> 'true', 'False' -> 'false'
if action_destructive_requires_name == 'True':
    action_destructive_requires_name = 'true'
else:
    action_destructive_requires_name = 'false'

xpack_security_enabled = str(config['configurations']['elasticsearch-config']['xpack_security_enabled'])

# 'True' -> 'true', 'False' -> 'false'
if xpack_security_enabled == 'True':
    xpack_security_enabled = 'true'
else:
    xpack_security_enabled = 'false'



