from rest_framework import serializers

from serial_port_logger.models import RecordingModel

class RecordingSerializer(serializers.Serializer):
    is_recording = serializers.BooleanField(required=True)

    def create(slef, validated_data):
        return RecordingModel.set(validated_data)

    def update(self, instance, validated_data):
        instance.is_recording = validated_data.get(
            'is_recording', instance.is_recording)
        return instance

    