# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Elasticsearch  service params
"""

from resource_management import *

config = Script.get_config()

es_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch_pid_dir']
es_master_pid_file = format("{es_pid_dir}/elasticsearch-master.pid")
es_slave_pid_file = format("{es_pid_dir}/elasticsearch-slave.pid")