import os
import random

from django.test import TestCase

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_in

from modules.serial_port_logger.models.serial_port_config_model import\
    SerialPortConfigModel
from modules.serial_port_logger.models.serial_port_config_data_access import\
    SerialPortConfigDataAccess
from integration_tests.random_serial_port_config_generator import\
    RandomSerialPortConfigGenerator

class TestSerialPortConfigurationModel(TestCase):

    def setUp(self):
        self._random_model_generator = RandomSerialPortConfigGenerator()
        (self._config_file, self._model_content) =\
            self._random_model_generator.generate()
        self._serial_ports = self._model_content['serial_ports'] 
        self._capture_data_access = SerialPortConfigModel._data_access 
        SerialPortConfigModel._data_access =\
            SerialPortConfigDataAccess(self._config_file)

    def tearDown(self):
        SerialPortConfigModel._data_access = self._capture_data_access
        os.remove(self._config_file)

    def assert_device_configs_equal_to(self, device, configs):
        assert_that(device.log_file, equal_to(configs['log_file']))
        assert_that(device.driver, equal_to(configs['driver']))
        assert_that(device.baud_rate, equal_to(configs['baud_rate']))
        assert_that(device.flow_control, 
            equal_to(configs['flow_control']))
        assert_that(device.parity, equal_to(configs['parity']))
        assert_that(device.stop_bits, equal_to(configs['stop_bits']))
        assert_that(device.character_size, 
            equal_to(configs['character_size']))

    def test_all_function_of_obecjts(self):
        devices = SerialPortConfigModel.objects.all()
        
        for device in devices:
            assert_that(device.device_name, is_in(self._serial_ports))
            device_configs = self._serial_ports[device.device_name]
            self.assert_device_configs_equal_to(device, device_configs)

    def test_get_function_of_objects(self):
        random_device_name = random.choice(list(self._serial_ports.keys()))
        device = SerialPortConfigModel.objects.get(random_device_name)
        device_configs = self._serial_ports[random_device_name]
        self.assert_device_configs_equal_to(device, device_configs)

    def test_create_function_of_objects(self):
        random_device_data = self._random_model_generator.generate_device_data()
        device = SerialPortConfigModel.objects.create(random_device_data)

        assert_that(random_device_data['device_name'], 
            equal_to(device.device_name))
        self.assert_device_configs_equal_to(device, random_device_data)

        device = SerialPortConfigModel.objects.get(
            random_device_data['device_name'])
        self.assert_device_configs_equal_to(device, random_device_data)
