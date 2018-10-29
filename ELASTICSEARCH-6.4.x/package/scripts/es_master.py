# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *


class ESMaster(Script):

    # Install Elasticsearch
    def install(self, env):
        import params
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
        Directory([params.es_master_base_dir, params.es_master_log_dir, params.es_master_pid_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.es_user,
                  group=params.es_group,
                  create_parents=True
                  )

        for es_path_data in params.master_path_data.split(","):
            Directory([es_path_data],
                      mode=0755,
                      cd_access='a',
                      owner=params.es_user,
                      group=params.es_group,
                      create_parents=True
                      )

        # Create install log
        File(params.es_master_install_log,
             mode=0644,
             owner=params.es_user,
             group=params.es_group,
             content=''
             )

        # Download Elasticsearch
        cmd = format("cd {es_master_base_dir}; wget {es_download_url} -O elasticsearch.tar.gz -a {es_master_install_log}")
        Execute(cmd, user=params.es_user)

        # Install Elasticsearch
        cmd = format("cd {es_master_base_dir}; tar -xf elasticsearch.tar.gz --strip-components=1")
        Execute(cmd, user=params.es_user)

        # Ensure all files owned by elasticsearch user
        cmd = format("chown -R {es_user}:{es_group} {es_master_base_dir}")
        Execute(cmd)

        # Remove Elasticsearch installation file
        cmd = format("cd {es_master_base_dir}; rm -fr elasticsearch.tar.gz")
        Execute(cmd, user=params.es_user)

        Execute('echo "Elasticsearch install complete"')

    # Configure Elasticsearch
    def configure(self, env):
        import params
        env.set_params(params)

        configurations = params.config['configurations']['elasticsearch-config']
        File(format("{es_master_conf_dir}/elasticsearch.yml"),
             content=Template("elasticsearch.master.yml.j2", configurations=configurations),
             owner=params.es_user,
             group=params.es_group
             )

        env_configurations = params.config['configurations']['elasticsearch-env']
        File(format("{es_master_conf_dir}/jvm.options"),
             content=Template("elasticsearch.jvm.options.j2", configurations=env_configurations),
             owner=params.es_user,
             group=params.es_group
             )

        cmd = format("chown -R {es_user}:{es_group} {es_master_base_dir}")
        Execute(cmd)

        Execute('echo "Configuration complete"')


    def stop(self, env):
        import params
        env.set_params(params)

        # Stop Elasticsearch
        """
            Kill the process by pid file, then check the process is running or not. If the process is still running after the kill
            command, it will try to kill with -9 option (hard kill)
            """
        pid_file = params.es_master_pid_file
        pid = os.popen('cat {pid_file}'.format(pid_file=pid_file)).read()

        process_id_exists_command = format("ls {pid_file} >/dev/null 2>&1 && ps -p {pid} >/dev/null 2>&1")

        kill_cmd = format("kill {pid}")
        Execute(kill_cmd,
                not_if=format("! ({process_id_exists_command})"))
        wait_time = 5

        hard_kill_cmd = format("kill -9 {pid}")
        Execute(hard_kill_cmd,
                not_if=format(
                    "! ({process_id_exists_command}) || ( sleep {wait_time} && ! ({process_id_exists_command}) )"),
                ignore_failures=True)
        try:
            Execute(format("! ({process_id_exists_command})"),
                    tries=20,
                    try_sleep=3,
                    )
        except:
            show_logs(params.es_master_log_dir, params.es_user)
            raise

        File(pid_file,
             action="delete"
             )

    def start(self, env):
        import params
        env.set_params(params)

        # Configure Elasticsearch
        self.configure(env)

        # Start Elasticsearch
        cmd = format("{es_master_base_dir}/bin/elasticsearch -d -p {es_master_pid_file}")
        Execute(cmd, user=params.es_user)

    def status(self, env):
        import status_params
        env.set_params(status_params)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.es_master_pid_file)


if __name__ == "__main__":
    ESMaster().execute()