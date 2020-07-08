import os
import io
import json
import random

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

    def assert_devices_equal_to_json_content(self, device_list, json_content): 
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

    def assert_device_equal_to_json_content(self, device, json_content): 
        assert_that(device.device_name, 
            equal_to(json_content['device_name']))
        assert_that(device.log_file, 
            equal_to(json_content['log_file']))
        assert_that(device.driver, equal_to(json_content['driver']))
        assert_that(device.baud_rate, 
            equal_to(json_content['baud_rate']))
        assert_that(device.flow_control, 
            equal_to(json_content['flow_control']))
        assert_that(device.parity, equal_to(json_content['parity']))
        assert_that(device.stop_bits, 
            equal_to(json_content['stop_bits']))
        assert_that(device.character_size, 
            equal_to(json_content['character_size']))

    def assert_equal_devices(self, device_list_1, device_list_2):
        assert_that(len(device_list_1), equal_to(len(device_list_2)))



    def test_get_all_resource(self):
        devices_before_request = SerialPortConfigModel.objects.all()
        
        response = self.client.get('/serial_ports/')

        stream = io.BytesIO(response.content)
        json_content =\
            self.prettify_json_content(self.json_parser.parse(stream))

        devices_after_request = SerialPortConfigModel.objects.all()

        assert_that(response.status_code, equal_to(200))
        self.assert_devices_equal_to_json_content(
            devices_after_request, json_content)

    def test_add_new_resource(self):
        devices_before_request = SerialPortConfigModel.objects.all()

        new_device_data = self._random_model_generator.generate_device_data()
        response = self.client.post(
            '/serial_ports/', 
            data=new_device_data, 
            content_type='application/json')

        devices_after_request = SerialPortConfigModel.objects.all()
        device = SerialPortConfigModel.objects.get(
            new_device_data['device_name'])

        assert_that(response.status_code, equal_to(201))
        assert_that(len(devices_after_request), 
            equal_to(len(devices_before_request) + 1))
        self.assert_device_equal_to_json_content(device, new_device_data)
        
    def test_get_a_resource(self):
        selected_random_device =\
            random.choice(SerialPortConfigModel.objects.all())

        response = self.client.get(
            '/serial_ports/' + selected_random_device.device_name)
        
        stream = io.BytesIO(response.content)
        json_content = self.json_parser.parse(stream)

        assert_that(response.status_code, equal_to(200))
        self.assert_device_equal_to_json_content(
            selected_random_device, json_content)
        
        