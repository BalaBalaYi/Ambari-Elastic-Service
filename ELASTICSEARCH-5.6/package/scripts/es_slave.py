# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *
from es_common import *

class ESlave(Script):

    # Install Elasticsearch
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.es_slave_pid_file property as
        # format('{es_slave_pid_file}')
        env.set_params(params)

        # Install dependent packages: no dependencies
        # self.install_packages(env)

        # Install elasticsearch
        do_install(env, params)

    # Configure Elasticsearch
    def configure(self, env):
        import params

        # This allows us to access the params.es_slave_pid_file property as
        # format('{es_slave_pid_file}')
        env.set_params(params)
        configurations = params.config['configurations']['elasticsearch-config']

        File(format("{es_conf_dir}/elasticsearch.yml"),
             content=Template("elasticsearch.slave.yml.j2", configurations=configurations),
             owner=params.es_user,
             group=params.es_group
             )
        # configure elasticsearch
        do_configure()


    def stop(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.es_slave_pid_file property as
        #  format('{es_slave_pid_file}')
        env.set_params(params)

        # Stop Elasticsearch
        kill_process(params.es_slave_pid_file, params.es_user, params.es_log_dir)
        # cmd = format("kill `cat {es_slave_pid_file}`")
        # Execute(cmd, user=params.es_user, only_if=format("test -f {es_slave_pid_file}"))

    def start(self, env):
        import params

        # This allows us to access the params.es_slave_pid_file property as
        #  format('{es_slave_pid_file}')
        env.set_params(params)

        # Configure Elasticsearch
        self.configure(env)

        # Start Elasticsearch
        cmd = format("{es_base_dir}/bin/elasticsearch -d -p {es_slave_pid_file}")
        Execute(cmd, user=params.es_user)

    def status(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.es_slave_pid_file property as
        #  format('{es_slave_pid_file}')
        env.set_params(status_params)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.es_slave_pid_file)

if __name__ == "__main__":
    ESlave().execute()