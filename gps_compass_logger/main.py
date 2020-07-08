import time

from ExitIfProcessIsRunning import * 
from GpsCompassLogger import *
from LedUserInterface import *

if __name__ == "__main__":
    
    exit_if_process_is_running = ExitIfProcessIsRunning()
    gps_compass_logger = GpsCompassLogger()

    def log_button_handler(channel):
        if(gps_compass_logger.is_started()):
            gps_compass_logger.stop_logging()
            return

        if(gps_compass_logger.is_connected()):
            gps_compass_logger.start_logging()

    led_user_interface = LedUserInterface(log_button_handler)
    
    while(True):
        if(gps_compass_logger.is_started()):
            led_user_interface.turn_log_led_on()
        else:
            led_user_interface.turn_log_led_off()

        if(not gps_compass_logger.is_started()):
            if(gps_compass_logger.is_connected()):
                led_user_interface.turn_connection_led_on()
            else:
                led_user_interface.turn_connection_led_off()

        time.sleep(0.5)
   
