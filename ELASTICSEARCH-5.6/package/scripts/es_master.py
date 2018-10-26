# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *
from es_common import *

class ESMaster(Script):

    # Install Elasticsearch
    def install(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.es_master_pid_file property as
        # format('{es_master_pid_file}')
        env.set_params(params)

        # Install dependent packages: no dependencies
        #self.install_packages(env)

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

        for es_path_data in params.path_data.split(","):
            Directory([es_path_data],
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
        Execute(cmd, user=params.es_user)

        # Install Elasticsearch
        cmd = format("cd {es_base_dir}; tar -xf elasticsearch.tar.gz --strip-components=1")
        Execute(cmd, user=params.es_user)

        # Ensure all files owned by elasticsearch user
        cmd = format("chown -R {es_user}:{es_group} {es_base_dir}")
        Execute(cmd)

        # Remove Elasticsearch installation file
        cmd = format("cd {es_base_dir}; rm -fr elasticsearch.tar.gz")
        Execute(cmd, user=params.es_user)

        Execute('echo "Elasticsearch install complete"')

    # Configure Elasticsearch
    def configure(self, env):
        import params

        # This allows us to access the params.es_master_pid_file property as
        # format('{es_master_pid_file}')
        env.set_params(params)
        configurations = params.config['configurations']['elasticsearch-config']

        File(format("{es_conf_dir}/elasticsearch.yml"),
             content=Template("elasticsearch.master.yml.j2", configurations=configurations),
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

        # This allows us to access the params.es_master_pid_file property as
        #  format('{es_master_pid_file}')
        env.set_params(params)

        # Stop Elasticsearch
        kill_process(params.es_master_pid_file, params.es_user, params.es_log_dir)
        # cmd = format("kill `cat {es_master_pid_file}`")
        # Execute(cmd, user=params.es_user, only_if=format("test -f {es_master_pid_file}"))

    def start(self, env):
        import params

        # This allows us to access the params.es_master_pid_file property as
        #  format('{es_master_pid_file}')
        env.set_params(params)

        # Configure Elasticsearch
        self.configure(env)

        # Start Elasticsearch
        cmd = format("{es_base_dir}/bin/elasticsearch -d -p {es_master_pid_file}")
        Execute(cmd, user=params.es_user)

    def status(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.es_master_pid_file property as
        #  format('{es_master_pid_file}')
        env.set_params(status_params)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.es_master_pid_file)

if __name__ == "__main__":
    ESMaster().execute()