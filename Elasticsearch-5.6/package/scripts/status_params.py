# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Elasticsearch  service params
"""

from resource_management import *

config = Script.get_config()

elastic_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch_pid_dir']
elastic_pid_file = format("{elasticsearch_pid_dir}/elasticsearch.pid")