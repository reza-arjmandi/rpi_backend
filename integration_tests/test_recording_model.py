from django.test import TestCase

from hamcrest import assert_that
from hamcrest import equal_to

from modules.test.random_generator import RandomGenerator
from serial_port_logger.models import RecordingModel
from modules.serial_port_logger.models.recording_model import Recording

class TestRecordingModel(TestCase):

    def setUp(self):
        self._random_generator = RandomGenerator()
        self.captured_state = RecordingModel._recording
        recording = Recording()
        recording.is_recording = self._random_generator.generate_bool()
        RecordingModel._recording = recording

    def tearDown(self):
        RecordingModel._recording = self.captured_state

    def test_get_function(self):
        record_object = RecordingModel.get()
        assert_that(record_object, equal_to(RecordingModel._recording))

    def test_set_function(self):
        random_data = {}
        random_data['is_recording'] = self._random_generator.generate_bool()
        result_obj = RecordingModel.set(random_data)
        assert_that(random_data['is_recording'], 
            equal_to(RecordingModel._recording.is_recording))
        assert_that(result_obj.is_recording, 
            equal_to(random_data['is_recording']))
