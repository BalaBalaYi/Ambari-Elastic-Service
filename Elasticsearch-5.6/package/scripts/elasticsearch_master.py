# -*- coding: utf-8 -*-

import sys
import os
import glob
import pwd
import grp
import signal
import time
from resource_management import *
from elastic_common import kill_process

class Master(Script):

    # Install Elasticsearch
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        # format('{elastic_pid_file}')
        env.set_params(params)

        # Install dependent packages
        self.install_packages(env)

        # Create user
        try:
            grp.getgrnam(params.es_group)
        except KeyError:
            Group(group_name=params.es_group)

        # Create group
        try:
            pwd.getpwnam(params.es_user)
        except KeyError:
            User(username=params.es_user,
                 gid=params.es_group,
                 groups=[params.es_group],
                 ignore_failures=True
                 )

        # Create directories
        Directory([params.es_base_dir, params.es_log_dir, params.es_pid_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.es_user,
                  group=params.es_group,
                  create_parents=True
                  )

        # Create install log
        File(params.es_install_log,
             mode=0644,
             owner=params.es_user,
             group=params.es_group,
             content=''
             )

        # Download Elasticsearch
        cmd = format("cd {es_base_dir}; wget {es_download_url} -O elasticsearch.tar.gz -a {es_install_log}")
        Execute(cmd, user=params.elastic_user)

        # Install Elasticsearch
        cmd = format("cd {es_base_dir}; tar -xf elasticsearch.tar.gz --strip-components=1")
        Execute(cmd, user=params.elastic_user)

        # Ensure all files owned by elasticsearch user
        cmd = format("chown -R {es_user}:{es_group} {es_base_dir}")
        Execute(cmd)

        # Remove Elasticsearch installation file
        cmd = format("cd {es_base_dir}; rm elasticsearch.tar.gz")
        Execute(cmd, user=params.elastic_user)

        Execute('echo "Elasticsearch install complete"')

    # Configure Elasticsearch
    def configure(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        # format('{elastic_pid_file}')
        env.set_params(params)
        configurations = params.config['configurations']['elasticsearch-config']

        File(format("{elastic_conf_dir}/elasticsearch.yml"),
             content=Template("elasticsearch.yml.j2",
                              configurations=configurations),
             owner=params.elastic_user,
             group=params.elastic_group
             )

        # Install HEAD and HQ puglins - these plugins are not currently supported by ES 5.x
        # cmd = format("{elastic_base_dir}/bin/elasticsearch-plugin install mobz/elasticserach-head")
        # Execute(cmd)

        # Attempt to remove X-Pack plugin
        cmd = format("{elastic_base_dir}/bin/elasticsearch-plugin remove x-pack")
        Execute(cmd)

        # Install X-Pack plugin
        cmd = format("{elastic_base_dir}/bin/elasticsearch-plugin install x-pack")
        Execute(cmd)

        # Ensure all files owned by elasticsearch user
        cmd = format("chown -R {elastic_user}:{elastic_group} {elastic_base_dir}")
        Execute(cmd)

        Execute('echo "Configuration complete"')

    def stop(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(params)

        # Stop Elasticsearch
        kill_process(params.elastic_pid_file, params.elastic_user, params.elastic_log_dir)
        # cmd = format("kill `cat {elastic_pid_file}`")
        # Execute(cmd, user=params.elastic_user, only_if=format("test -f {elastic_pid_file}"))

    def start(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(params)

        # Configure Elasticsearch
        self.configure(env)

        # Start Elasticsearch
        cmd = format("{elastic_base_dir}/bin/elasticsearch -d -p {elastic_pid_file}")
        Execute(cmd, user=params.elastic_user)

    def status(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(status_params)

        # try:
        #    pid_file = glob.glob(status_params.elastic_pid_file)[0]
        # except IndexError:
        #    pid_file = ''

        # Use built-in method to check status using pidfile
        check_process_status(status_params.elastic_pid_file)

    if __name__ == "__main__":
        Master().execute()