
import io

from django.test import TestCase
from django.test import Client
from rest_framework.parsers import JSONParser

from hamcrest import assert_that
from hamcrest import equal_to

# from serial_port_logger.models import RecordingModel

# from modules.test.random_generator import RandomGenerator

# class ModelEqualityGuard:
    
#     def __init__(self, model):
#         self._model = model
#         self.state_when_init = self._model.get()

#     def __del__(self):
#         state_when_del = self._model.get()
#         ModelEqualityGuard.assert_equal_states(
#             self.state_when_init, state_when_del)
    
#     def assert_equal_states(state_1, state_2):
#         assert_that(state_1, equal_to(state_1))

# class TestRecordingResource(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.json_parser = JSONParser()
#         self._random_generator = RandomGenerator() 

#     def json_to_dict(self, json):
#         stream = io.BytesIO(json)
#         return self.json_parser.parse(stream)

    # def test_get_resource(self):
    #     model_equality_guard = ModelEqualityGuard(RecordingModel)

    #     response = self.client.get('/recording/')

    #     assert_that(response.status_code, equal_to(200))
        
    #     json_content = self.json_to_dict(response.content)
    #     assert_that(json_content['is_recording'], 
    #         equal_to(RecordingModel.get()))

    # def test_update_resource(self):
    #     updated_state={}
    #     updated_state['is_recording'] = self._random_generator.generate_bool()

    #     response = self.client.put(
    #         '/recording/',
    #         data=updated_state, 
    #         content_type='application/json')

    #     assert_that(response.status_code, equal_to(200))

    #     json_content = self.json_to_dict(response.content)
    #     assert_that(json_content['is_recording'], 
    #         equal_to(updated_state['is_recording']))
    #     assert_that(RecordingModel.get(), 
    #         equal_to(updated_state['is_recording']))
        

    

