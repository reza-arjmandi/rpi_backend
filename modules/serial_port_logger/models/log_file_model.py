
import json
import os
import re

class LogFile:
    device_name = None
    file_name = None
    file_path = None

    def __init__(self, data_access):
        self._data_access = data_access
        
    def __eq__(self, other):
        equal = False
        try:
            equal = self.file_name == other.file_name\
                and self.file_path == other.file_path\
                and self.device_name == other.device_name
        except:
            equal = False
        return equal


    def __ne__(self, other):
        return not self.__eq__(other)

    def save(self):
        self._data_access.insert_or_update(self)

    def delete(self):
        self._data_access.delete(self)


class LogFileDataAccess:
    _device_log_map = None
    _log_dir_path = None

    def __init__(self, log_dir_path):
        self._log_dir_path = log_dir_path
        
    def insert_or_update(self, log_file):
        self._read_map()
        self._device_log_map[log_file.device_name] = log_file.file_path
        self._apply_map()

    def delete(self, log_file):
        self._read_map()
        if log_file.device_name in self._device_log_map:
            del self._device_log_map[log_file.device_name]
            self._apply_map()

    def get_all(self):
        self._read_map()
        log_files = []
        for (device_name, file_path) in self._device_log_map.items():
            log_file = LogFile(self)
            log_file.device_name = device_name
            log_file.file_name = '{}_log.txt'.format(device_name)
            log_file.file_path = file_path
            log_files.append(log_file)
        return log_files

    def get(self, device_name):
        self._read_map()
        log_file = None
        if device_name in self._device_log_map:
            log_file = LogFile(self)
            log_file.device_name = device_name
            log_file.file_name = '{}_log.txt'.format(device_name)
            log_file.file_path = self._device_log_map[device_name]
        return log_file

    def _read_map(self):
        list_of_files = os.listdir(self._log_dir_path)

        pattern = r'(.*)_log.txt'
        device_logs_map = {}

        for file in list_of_files:
            match = re.search(pattern, file)
            if not match:
                continue

            device_name = match.group(1)
            device_logs_map[device_name] =\
                os.path.join(self._log_dir_path, file)

        self._device_log_map = device_logs_map

    def _apply_map(self):
        list_of_files = os.listdir(self._log_dir_path)
        pattern = '^(.*)_log.txt$'
        
        for file in list_of_files:
            match = re.search(pattern, file)
            if not match:
                continue

            device_name = match.group(1)
            if device_name in self._device_log_map:
                continue

            os.remove(os.path.join(self._log_dir_path, file))

        for file_path in self._device_log_map.values():
            if os.path.exists(file_path):
                continue
            open(file_path, 'w')

class LogFileModel:
    _log_files_dir_path = os.path.join(os.getcwd(), 'log_files')
    _data_access = LogFileDataAccess(_log_files_dir_path)

    class objects:

        def create(data):
            log_file = LogFile(LogFileModel._data_access)
            log_file.device_name = data['device_name']
            log_file.file_name = '{}_log.txt'.format(data['device_name'])
            log_file.file_path = os.path.join(
                LogFileModel._log_files_dir_path, log_file.file_name)
            return log_file

        def all():
            return LogFileModel._data_access.get_all()

        def get(device_name):
            return LogFileModel._data_access.get(device_name)