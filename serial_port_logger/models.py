from django.db import models
import json

class SerialPortDevice:
    device_name = None
    log_file = None
    driver = None
    baud_rate = None
    flow_control = None
    parity = None
    stop_bits = None
    character_size = None

    def __init__(self, data_access):
        self._data_access = data_access

    def save(self):
        self._data_access.insert_or_update(self)

    def delete(self):
        self._data_access.delete(self)

class SerialPortConfigDataAccess:
    _config_content = None
    _config_file_path = None

    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        
    def insert_or_update(self, device):
        self._read_config()
        self._config_content['serial_ports'][device.device_name] = {
            'log_file' : device.log_file,
            'driver' : device.driver,
            'baud_rate' : device.baud_rate,
            'flow_control' : device.flow_control,
            'parity' : device.parity,
            'stop_bits' : device.stop_bits,
            'character_size' : device.character_size,
        }
        self._save_content()

    def delete(self, device):
        self._read_config()
        if device.device_name in self._config_content['serial_ports']:
            del self._config_content['serial_ports'][device.device_name]
            self._save_content()

    def get_all(self):
        self._read_config()
        devices = []
        for (device_name, configs) in self._config_content['serial_ports'].items():
            device = SerialPortDevice(self)
            device.device_name = device_name
            device.log_file = configs['log_file']
            device.driver = configs['driver']
            device.baud_rate = configs['baud_rate']
            device.flow_control = configs['flow_control']
            device.parity = configs['parity']
            device.stop_bits = configs['stop_bits']
            device.character_size = configs['character_size']
            devices.append(device)
        return devices

    def get(self, device_name):
        self._read_config()
        device = None
        if device_name in self._config_content['serial_ports']:
            configs = self._config_content['serial_ports'][device_name]
            device = SerialPortDevice(self)
            device.device_name = device_name
            device.log_file = configs['log_file']
            device.driver = configs['driver']
            device.baud_rate = configs['baud_rate']
            device.flow_control = configs['flow_control']
            device.parity = configs['parity']
            device.stop_bits = configs['stop_bits']
            device.character_size = configs['character_size']
        return device

    def _read_config(self):
        content = None 
        
        with open(self._config_file_path) as file:
            content = file.read()
        
        if content:
            self._config_content = json.loads(content)

    def _save_content(self):
        with open(self._config_file_path, 'w') as file:
            json.dump(self._config_content, file)

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
