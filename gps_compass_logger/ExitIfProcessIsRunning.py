import os
import sys

class ExitIfProcessIsRunning:

    def __init__(self):
        self._pidfile = "/tmp/gps_compass_logger.pid"
        self._pidfile_created = False
        self._exit_if_pidfile_exist()
        self._create_pidfile()

    def __del__(self):
        if(self._pidfile_created):
            os.unlink(self._pidfile)

    def _exit_if_pidfile_exist(self):
        if(os.path.isfile(self._pidfile)):
            print("{0} is already exists, existing".format(self._pidfile))
            sys.exit()
    
    def _create_pidfile(self):
        pid = str(os.getpid())
        open(self._pidfile, "w").write(pid)
        self._pidfile_created = True