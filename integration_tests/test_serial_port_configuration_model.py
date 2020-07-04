import os

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
        self._capture_data_access = SerialPortConfigModel._data_access 
        SerialPortConfigModel._data_access =\
            SerialPortConfigDataAccess(self._config_file)

    def tearDown(self):
        SerialPortConfigModel._data_access = self._capture_data_access
        os.remove(self._config_file)

    def test_all_function_of_obecjts(self):
        devices = SerialPortConfigModel.objects.all()
        
        for device in devices:
            serial_ports = self._model_content['serial_ports'] 
            assert_that(device.device_name, is_in(serial_ports))

            device_configs =\
                self._model_content['serial_ports'][device.device_name]
            assert_that(device.log_file, equal_to(device_configs['log_file']))
            assert_that(device.driver, equal_to(device_configs['driver']))
            assert_that(device.baud_rate, equal_to(device_configs['baud_rate']))
            assert_that(device.flow_control, 
                equal_to(device_configs['flow_control']))
            assert_that(device.parity, equal_to(device_configs['parity']))
            assert_that(device.stop_bits, equal_to(device_configs['stop_bits']))
            assert_that(device.character_size, 
                equal_to(device_configs['character_size']))
        
