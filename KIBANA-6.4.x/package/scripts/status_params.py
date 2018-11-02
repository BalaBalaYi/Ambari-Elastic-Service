# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Kibana  service params
"""

from resource_management import *

config = Script.get_config()

pid_file_dir = config['configurations']['kibana-env']['pid.file.dir']
pid_file = format("{pid_file_dir}/kibana.pid")