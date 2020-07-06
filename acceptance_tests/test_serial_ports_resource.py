import os
import io

from rest_framework.parsers import JSONParser
from django.test import TestCase
from django.test import Client

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_in

from integration_tests.random_serial_port_config_generator import\
    RandomSerialPortConfigGenerator
from modules.test.random_generator import RandomGenerator
from modules.serial_port_logger.models.serial_port_config_model import\
    SerialPortConfigModel
from modules.serial_port_logger.models.serial_port_config_data_access import\
    SerialPortConfigDataAccess

class TestSerialPortsResource(TestCase):
        
    def setUp(self):
        self._random_model_generator = RandomSerialPortConfigGenerator()
        self._random_generator = RandomGenerator()
        (self._config_file, self._model_content) =\
            self._random_model_generator.generate()
        self._serial_ports = self._model_content['serial_ports'] 
        self._capture_data_access = SerialPortConfigModel._data_access 
        SerialPortConfigModel._data_access =\
            SerialPortConfigDataAccess(self._config_file)
        self.client = Client()
        self.json_parser = JSONParser()

    def tearDown(self):
        SerialPortConfigModel._data_access = self._capture_data_access
        os.remove(self._config_file)

    def prettify_json_content(self, device_list_content):
        result = {}
        for device in device_list_content:
            device_name = device['device_name']
            result[device_name] = {}
            result[device_name]['log_file'] = device['log_file']
            result[device_name]['driver'] = device['driver']
            result[device_name]['baud_rate'] = device['baud_rate']
            result[device_name]['flow_control'] = device['flow_control']
            result[device_name]['parity'] = device['parity']
            result[device_name]['stop_bits'] = device['stop_bits']
            result[device_name]['character_size'] = device['character_size']
        return result

    def assert_device_equal_to_json_content(self, device_list, json_content): 
        assert_that(len(device_list), equal_to(len(json_content)))
        for device in device_list:
            device_name = device.device_name
            device_json_content = json_content[device_name]

            assert_that(device_name, is_in(json_content))
            assert_that(device.log_file, 
                equal_to(device_json_content['log_file']))
            assert_that(device.driver, equal_to(device_json_content['driver']))
            assert_that(device.baud_rate, 
                equal_to(device_json_content['baud_rate']))
            assert_that(device.flow_control, 
                equal_to(device_json_content['flow_control']))
            assert_that(device.parity, equal_to(device_json_content['parity']))
            assert_that(device.stop_bits, 
                equal_to(device_json_content['stop_bits']))
            assert_that(device.character_size, 
                equal_to(device_json_content['character_size']))

    def test_get_all_resource(self):
        response = self.client.get('/serial_ports/')

        stream = io.BytesIO(response.content)
        json_content =\
            self.prettify_json_content(self.json_parser.parse(stream))

        devices = SerialPortConfigModel.objects.all()
        assert_that(response.status_code, equal_to(200))
        self.assert_device_equal_to_json_content(devices, json_content)