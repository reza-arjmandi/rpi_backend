from modules.serial_port_logger.models.serial_port_config_data_access import\
    SerialPortConfigDataAccess
from modules.serial_port_logger.models.serial_port_device import\
    SerialPortDevice

class SerialPortConfigModel:
    _data_access = SerialPortConfigDataAccess('config.json')
    
    class objects:

        def create(data):
            device = SerialPortDevice(SerialPortConfigModel._data_access)
            device.device_name = data['device_name']
            device.log_file = data['log_file']
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
