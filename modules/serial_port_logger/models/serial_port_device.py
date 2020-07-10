
from modules.serial_port_logger.models.log_file_model import LogFileModel

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
        
    def __eq__(self, other):
        equal = False
        try:
            equal = self.device_name == other.device_name\
                and self.log_file == other.log_file\
                and self.driver == other.driver\
                and self.baud_rate == other.baud_rate\
                and self.flow_control == other.flow_control\
                and self.parity == other.parity\
                and self.stop_bits == other.stop_bits\
                and self.character_size == other.character_size
        except:
            equal = False
        return equal


    def __ne__(self, other):
        return not self.__eq__(other)

    def save(self):
        self._data_access.insert_or_update(self)

    def delete(self):
        self._data_access.delete(self)
        log_file = LogFileModel.objects.get(self.device_name)
        log_file.delete()

