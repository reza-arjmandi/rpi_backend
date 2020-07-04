
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

    def save(self):
        self._data_access.insert_or_update(self)

    def delete(self):
        self._data_access.delete(self)
