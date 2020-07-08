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
from hamcrest import contains_inanyorder

from integration_tests.random_serial_port_config_generator import\
    RandomSerialPortConfigGenerator
from modules.test.random_generator import RandomGenerator
from modules.serial_port_logger.models.serial_port_config_model import\
    SerialPortConfigModel
from modules.serial_port_logger.models.serial_port_config_data_access import\
    SerialPortConfigDataAccess

class ModelEqualityGuard:
    
    def __init__(self, model):
        self._model = model
        self.objects_when_init = self._model.objects.all()

    def __del__(self):
        objects_when_del = self._model.objects.all()
        ModelEqualityGuard.assert_equal_objects(
            self.objects_when_init, objects_when_del)
    
    def assert_equal_objects(object_list_1, object_list_2):
        assert_that(len(object_list_1), equal_to(len(object_list_2)))
        assert_that(object_list_1, contains_inanyorder(*object_list_2))
        
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
            self.assert_device_equal_to_json_content(
                device, device_json_content, check_device_name=False)

    def assert_device_equal_to_json_content(
        self, device, json_content, check_device_name=True):
        if check_device_name: 
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
    
    def assert_device_updated(self, 
        devices_before_request, 
        device_to_be_going_to_updated, 
        expected_updated_device_data,
        response):
        response_content = self.json_to_dict(response.content)
        assert_that(response.status_code, equal_to(200))

        devices_after_request = SerialPortConfigModel.objects.all()

        assert_that(len(devices_before_request),\
            equal_to(len(devices_after_request)))
        assert_that(response_content, equal_to(expected_updated_device_data))

        updated_device = SerialPortConfigModel.objects.get(
            expected_updated_device_data['device_name'])
        self.assert_device_equal_to_json_content(
            updated_device, expected_updated_device_data)

        devices_before_request.remove(device_to_be_going_to_updated)
        devices_before_request.append(updated_device)
        ModelEqualityGuard.assert_equal_objects(
            devices_before_request, devices_after_request)

    def json_to_dict(self, json):
        stream = io.BytesIO(json)
        return self.json_parser.parse(stream)

    def update_device(self, device, updated_field):
        updated_device_data = {}
        updated_device_data['device_name'] =device.device_name
        updated_device_data['log_file'] = device.log_file
        updated_device_data['driver'] = device.driver
        updated_device_data['baud_rate'] = device.baud_rate
        updated_device_data['flow_control'] =\
            device.flow_control
        updated_device_data['parity'] = device.parity
        updated_device_data['stop_bits'] = device.stop_bits
        updated_device_data['character_size'] =\
            device.character_size
        updated_device_data[updated_field['field']] = updated_field['value']
        return updated_device_data

    def choose_a_random_device(self):
        devices = SerialPortConfigModel.objects.all()
        selected_random_device = random.choice(devices)
        return (selected_random_device, devices)

    def __test_update_device__(self, updated_data):
        (selected_random_device, device_before_request) =\
            self.choose_a_random_device()
        resource_url = '/serial_ports/{0}/'.format(
            selected_random_device.device_name)

        updated_device_data = self.update_device(
            selected_random_device, 
            updated_data)

        response = self.client.put(
            resource_url,
            data=updated_device_data, 
            content_type='application/json')

        self.assert_device_updated(
            device_before_request, 
            selected_random_device, 
            updated_device_data, 
            response)

    def test_get_all_resource(self):
        model_equality_guard = ModelEqualityGuard(SerialPortConfigModel)
        
        response = self.client.get('/serial_ports/')

        json_content =\
            self.prettify_json_content(self.json_to_dict(response.content))

        devices = SerialPortConfigModel.objects.all()
        assert_that(response.status_code, equal_to(200))
        self.assert_devices_equal_to_json_content(
            devices, json_content)

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
        
        devices_before_request.append(device)
        ModelEqualityGuard.assert_equal_objects(
            devices_before_request, devices_after_request)
        
    def test_get_a_resource(self):
        model_equality_guard = ModelEqualityGuard(SerialPortConfigModel)

        selected_random_device =\
            random.choice(SerialPortConfigModel.objects.all())
        resource_url = '/serial_ports/{0}/'.format(
            selected_random_device.device_name)
        response = self.client.get(resource_url)

        json_content = self.json_to_dict(response.content)

        assert_that(response.status_code, equal_to(200))
        self.assert_device_equal_to_json_content(
            selected_random_device, json_content)

    def test_update_device_name(self):
        self.__test_update_device__({'field' : 'device_name', 
            'value' : self._random_generator.generate_string(2,10)})

    def test_update_log_file(self):
        self.__test_update_device__({'field' : 'log_file', 
            'value' : self._random_generator.generate_string(2,10)})

    def test_update_driver(self):
        self.__test_update_device__({'field' : 'driver', 
            'value' : self._random_generator.generate_string(2,10)})

    def test_update_baud_rate(self):
        self.__test_update_device__({'field' : 'baud_rate', 
            'value' : random.choice(SerialPortConfigModel.baud_rate_choices)})

    def test_update_flow_control(self):
        self.__test_update_device__({'field' : 'flow_control', 
            'value' 
            : random.choice(SerialPortConfigModel.flow_control_choices)})

    def test_update_parity(self):
        self.__test_update_device__({'field' : 'parity', 
            'value' : random.choice(SerialPortConfigModel.parity_choices)})

    def test_update_stop_bits(self):
        self.__test_update_device__({'field' : 'stop_bits', 
            'value' : random.choice(SerialPortConfigModel.stop_bits_choices)})

    def test_update_character_size(self):
        self.__test_update_device__({'field' : 'character_size', 
            'value' : self._random_generator.generate_int(1,100)})

    def test_delete_a_resource(self):
        devices_before_request = SerialPortConfigModel.objects.all()
        selected_random_device = random.choice(devices_before_request)

        resource_url = '/serial_ports/{0}/'.format(
            selected_random_device.device_name)
        response = self.client.delete(resource_url)

        devices_after_request = SerialPortConfigModel.objects.all()

        assert_that(response.status_code, equal_to(204))
        assert_that(len(devices_after_request), 
            equal_to(len(devices_before_request) - 1))
        devices_after_request.append(selected_random_device)
        ModelEqualityGuard.assert_equal_objects(
            devices_before_request, devices_after_request)