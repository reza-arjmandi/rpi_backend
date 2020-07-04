
import json
import random

from modules.test.random_generator import RandomGenerator
from modules.serial_port_logger.models.serial_port_config_model import\
    SerialPortConfigModel

class RandomSerialPortConfigGenerator:

    _random_generator = RandomGenerator()
    _model_contetnt = {'serial_ports': {}}

    def generate_device_data(self):
        device_data = {}
        device_data['device_name'] =\
            self._random_generator.generate_string(2, 10) 
        device_data['log_file'] = self._generate_random_path() 
        device_data['driver'] = self._generate_random_path() 
        device_data['baud_rate'] =\
            self._random_choose(SerialPortConfigModel.baud_rate_choices) 
        device_data['flow_control'] =\
            self._random_choose(SerialPortConfigModel.flow_control_choices) 
        device_data['parity'] =\
            self._random_choose(SerialPortConfigModel.parity_choices) 
        device_data['stop_bits'] =\
            self._random_choose(SerialPortConfigModel.stop_bits_choices) 
        device_data['character_size'] =\
            self._random_generator.generate_int(8, 100)
        return device_data

    def generate(self):
        _file_name = self._random_generator.generate_string(2, 10)
        number_of_device =  self._random_generator.generate_int(1, 100)
        for num in range(number_of_device):
            device_name = self._random_generator.generate_string(2, 10)
            self._model_contetnt['serial_ports'][device_name] = {}
            self._model_contetnt['serial_ports'][device_name]['log_file'] =\
                self._generate_random_path()
            self._model_contetnt['serial_ports'][device_name]['driver'] =\
                self._generate_random_path()
            self._model_contetnt['serial_ports'][device_name]['baud_rate'] =\
                self._random_choose(SerialPortConfigModel.baud_rate_choices)
            self._model_contetnt['serial_ports'][device_name]['flow_control'] =\
                self._random_choose(SerialPortConfigModel.flow_control_choices)
            self._model_contetnt['serial_ports'][device_name]['parity'] =\
                self._random_choose(SerialPortConfigModel.parity_choices)
            self._model_contetnt['serial_ports'][device_name]['stop_bits'] =\
                self._random_choose(SerialPortConfigModel.stop_bits_choices)
            self._model_contetnt['serial_ports'][device_name][
                'character_size'] = self._random_generator.generate_int(8, 100)
        self._save_content(_file_name)
        return (_file_name, self._model_contetnt)

    def _generate_random_path(self):
        path_level = self._random_generator.generate_int(1, 5)
        return self._random_generator.generate_path(path_level)

    def _random_choose(self, choices):
        return random.choice(choices)

    def _save_content(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self._model_contetnt, file)