import subprocess
import signal

class GpsCompassLogger:

    def __init__(self):
        self._config_argument = "--CONFIG_FILE=/home/pi/gps_compass_logger/config.json"
        self._is_connected_argument = "--IS-CONNECTED"
        self._process_name = "serial_port_logger"
        self._is_started = False
        self._process = None

    def _diagnose_connection(self, line):
        if(line.find("gps is connected successfully") 
        or line.find("compass is connected successfully")):
            return True
    
    def is_connected(self):
        result = False
        process = subprocess.Popen([
            self._process_name, 
            self._config_argument, 
            self._is_connected_argument], stdout=subprocess.PIPE)
        lines = process.stdout.readlines()
        if(self._diagnose_connection(lines[0]) 
        and self._diagnose_connection(lines[1])):
            result = True

        return result
        

    def is_started(self):
        return self._is_started

    def start_logging(self):
        self._process = subprocess.Popen([
            self._process_name, self._config_argument])
        self._is_started = True
        
    def stop_logging(self):
        if(self.is_started()):
            self._process.terminate()
            self._is_started = False
