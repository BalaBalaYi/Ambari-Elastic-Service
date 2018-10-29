# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *

class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        time.sleep(5)
        check_process_status(params.es_master_pid_file)


if __name__ == "__main__":
    ServiceCheck().execute()