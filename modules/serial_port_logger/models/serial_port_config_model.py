from modules.serial_port_logger.models.serial_port_config_data_access import\
    SerialPortConfigDataAccess
from modules.serial_port_logger.models.serial_port_device import\
    SerialPortDevice

from modules.serial_port_logger.models.log_file_model import LogFileModel

class SerialPortConfigModel:
    _data_access = SerialPortConfigDataAccess('config.json')

    baud_rate_choices = [
        110, 300, 600, 1200, 2400, 4800, 9600, 14400, 
        19200, 38400, 57600, 115200, 128000, 256000]
    flow_control_choices = ['hardware', 'software', 'none']
    parity_choices = ['none', 'odd', 'even']
    stop_bits_choices = [1, 1.5, 2]
    
    class objects:

        def create(data):
            device = SerialPortDevice(SerialPortConfigModel._data_access)
            device.device_name = data['device_name']

            log_file_data = {}
            log_file_data['device_name'] = data['device_name']
            log_file = LogFileModel.objects.create(log_file_data)
            log_file.save()

            device.log_file = log_file.file_path
            device.driver = data['driver']
            device.baud_rate = data['baud_rate']
            device.flow_control = data['flow_control']
            device.parity = data['parity']
            device.stop_bits = data['stop_bits']
            device.character_size = data['character_size']
            device.save()
            return device

        def all():
            return SerialPortConfigModel._data_access.get_all()

        def get(device_name):
            return SerialPortConfigModel._data_access.get(device_name)
