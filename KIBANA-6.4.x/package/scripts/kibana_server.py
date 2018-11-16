# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *


class KibanaServer(Script):

    # Install Kibana
    def install(self, env):
        import params
        env.set_params(params)

        # Install dependent packages: no dependencies
        #self.install_packages(env)

        # Create user
        try:
            grp.getgrnam(params.kibana_group)
        except KeyError:
            Group(group_name=params.kibana_group)

        # Create group
        try:
            pwd.getpwnam(params.kibana_user)
        except KeyError:
            User(username=params.kibana_user,
                 gid=params.kibana_group,
                 groups=[params.kibana_group],
                 ignore_failures=True
                 )

        # Create directories
        Directory([params.kibana_base_dir, params.logging_dest_dir, params.pid_file_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.kibana_user,
                  group=params.kibana_group,
                  create_parents=True
                  )

        # Download Kibana
        cmd = format("cd {kibana_base_dir}; wget {kibana_download_url} -O kibana.tar.gz")
        Execute(cmd, user=params.kibana_user)

        # Install Kibana
        cmd = format("cd {kibana_base_dir}; tar -xf kibana.tar.gz --strip-components=1")
        Execute(cmd, user=params.kibana_user)

        # Ensure all files owned by Kibana user
        cmd = format("chown -R {kibana_user}:{kibana_group} {kibana_base_dir}")
        Execute(cmd)

        # Remove Kibana installation file
        cmd = format("cd {kibana_base_dir}; rm -fr kibana.tar.gz")
        Execute(cmd, user=params.kibana_user)

        Execute('echo "Kibana install complete"')

    # Configure Kibana
    def configure(self, env):
        import params
        env.set_params(params)

        configurations = params.config['configurations']['kibana-config']
        File(format("{kibana_base_dir}/config/kibana.yml"),
             content=Template("kibana.yml.j2", configurations=configurations),
             owner=params.kibana_user,
             group=params.kibana_group
             )

        cmd = format("chown -R {kibana_user}:{kibana_group} {kibana_base_dir}")
        Execute(cmd)

        # Make sure pid directory exist
        Directory([params.pid_file_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.kibana_user,
                  group=params.kibana_group,
                  create_parents=True
                  )

        Execute('echo "Configuration complete"')


    def stop(self, env):
        import params
        env.set_params(params)

        # Stop Kibana
        """
            Kill the process by pid file, then check the process is running or not. If the process is still running after the kill
            command, it will try to kill with -9 option (hard kill)
            """
        pid_file = params.pid_file
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
            show_logs(params.logging_dest_dir, params.kibana_user)
            raise

        File(pid_file,
             action="delete"
             )

    def start(self, env):
        import params
        env.set_params(params)

        # Configure Kibana
        self.configure(env)

        # Start Kibana
        cmd = format("nohup {kibana_base_dir}/bin/kibana -l {logging_dest} &")
        Execute(cmd, user=params.kibana_user)

    def status(self, env):
        import status_params
        env.set_params(status_params)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.pid_file)


if __name__ == "__main__":
    KibanaServer().execute()