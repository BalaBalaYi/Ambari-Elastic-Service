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



java64_home = config['hostLevelParams']['java_home']

hostname = config['hostname']


# es env
es_user = config['configurations']['elasticsearch-env']['elasticsearch_user']
es_group = config['configurations']['elasticsearch-env']['elasticsearch_group']

es_master_base_dir = config['configurations']['elasticsearch-env']['elasticsearch_base_dir'] + '/master'
es_slave_base_dir = config['configurations']['elasticsearch-env']['elasticsearch_base_dir'] + '/slave'

es_master_home = es_master_base_dir
es_master_bin = es_master_base_dir + '/bin'
es_slave_home = es_slave_base_dir
es_slave_bin = es_slave_base_dir + '/bin'

es_master_conf_dir = es_master_base_dir + '/config'
es_slave_conf_dir = es_slave_base_dir + '/config'

es_master_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch_pid_dir'] + '/master'
es_slave_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch_pid_dir'] + '/slave'

es_master_pid_file = format("{es_master_pid_dir}/elasticsearch-master.pid")
es_slave_pid_file = format("{es_slave_pid_dir}/elasticsearch-slave.pid")

es_download_url = config['configurations']['elasticsearch-env']['elasticsearch_download_url']

# jvm
heap_size = config['configurations']['elasticsearch-env']['elasticsearch_heap_size']


# es config
cluster_name = config['configurations']['elasticsearch-config']['cluster_name']
hostname = config['hostname']
node_attr_rack = config['configurations']['elasticsearch-config']['node_attr_rack']

data_dir = config['configurations']['elasticsearch-config']['path_data']

es_master_log_dir = config['configurations']['elasticsearch-config']['path_logs'] + '/master'
es_slave_log_dir = config['configurations']['elasticsearch-config']['path_logs'] + '/slave'

es_master_install_log = es_master_log_dir + '/elasticsearch-install.log'
es_slave_install_log = es_slave_log_dir + '/elasticsearch-install.log'

# multi data path
master_path_data = ','.join(x + '/master' for x in data_dir.split(','))
slave_path_data = ','.join(x + '/slave' for x in data_dir.split(','))
# single log path
master_path_logs = es_master_log_dir
slave_path_logs = es_slave_log_dir

bootstrap_memory_lock = str(config['configurations']['elasticsearch-config']['bootstrap_memory_lock'])

# 'True' -> 'true', 'False' -> 'false'
if bootstrap_memory_lock == 'True':
    bootstrap_memory_lock = 'true'
else:
    bootstrap_memory_lock = 'false'

network_host = config['configurations']['elasticsearch-config']['network_host']
#http_port = config['configurations']['elasticsearch-config']['http_port']

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




