import os

from django.test import TestCase

from hamcrest import assert_that
from hamcrest import equal_to

from modules.serial_port_logger.serializers.serial_port_serializer import\
    SerialPortSerializer
from integration_tests.random_serial_port_config_generator import\
    RandomSerialPortConfigGenerator
from modules.serial_port_logger.models.serial_port_config_data_access import\
    SerialPortConfigDataAccess
from modules.serial_port_logger.models.serial_port_config_model import\
    SerialPortConfigModel
from modules.test.random_generator import RandomGenerator

class TestSerialPortSerializer(TestCase):

    def setUp(self):
        self._random_model_generator = RandomSerialPortConfigGenerator()
        self._random_generator = RandomGenerator()
        (self._config_file, self._model_content) =\
            self._random_model_generator.generate()
        self._serial_ports = self._model_content['serial_ports'] 
        self._capture_data_access = SerialPortConfigModel._data_access 
        SerialPortConfigModel._data_access =\
            SerialPortConfigDataAccess(self._config_file)
        self._random_data = self._random_model_generator.generate_device_data()

    def tearDown(self):
        SerialPortConfigModel._data_access = self._capture_data_access
        os.remove(self._config_file)

    def test_device_name_must_be_required(self):
        del self._random_data['device_name']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_device_name_must_not_be_blank(self):
        self._random_data['device_name'] = ''
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_log_file_must_be_required(self):
        del self._random_data['log_file']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_log_file_must_not_be_blank(self):
        self._random_data['log_file'] = ''
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_driver_must_be_required(self):
        del self._random_data['driver']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_driver_must_not_be_blank(self):
        self._random_data['driver'] = ''
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_baud_rate_must_be_required(self):
        del self._random_data['baud_rate']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_baud_rate_must_only_accept_valid_values(self):
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(True))

        self._random_data['baud_rate'] = '22222'
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_flow_control_must_be_required(self):
        del self._random_data['flow_control']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_flow_control_must_only_accept_valid_values(self):
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(True))

        self._random_data['flow_control'] =\
            self._random_generator.generate_string(2, 10)
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_parity_must_be_required(self):
        del self._random_data['parity']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_parity_must_only_accept_valid_values(self):
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(True))

        self._random_data['parity'] =\
            self._random_generator.generate_string(2, 10)
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_stop_bits_must_be_required(self):
        del self._random_data['stop_bits']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_stop_bits_must_only_accept_valid_values(self):
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(True))

        self._random_data['stop_bits'] = '232'
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_character_size_must_be_required(self):
        del self._random_data['character_size']
        serializer = SerialPortSerializer(data=self._random_data)
        assert_that(serializer.is_valid(), equal_to(False))

    def test_persistence(self):
        serializer = SerialPortSerializer(data=self._random_data)
        if serializer.is_valid():
            device = serializer.save()

        assert_that(device.device_name, 
            equal_to(self._random_data['device_name']))
        self.assert_device_configs_equal_to(device, self._random_data)

        saved_device = SerialPortConfigModel.objects.get(device.device_name)
        self.assert_device_configs_equal_to(saved_device, self._random_data)

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