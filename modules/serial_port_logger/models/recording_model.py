
class Recording:
    is_recording = False

class RecordingModel:
    
    _recording = Recording()

    def get():
        return RecordingModel._recording

    def set(data):
        RecordingModel._recording.is_recording = data['is_recording']
        return RecordingModel._recording
