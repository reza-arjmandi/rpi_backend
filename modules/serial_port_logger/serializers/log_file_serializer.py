from rest_framework import serializers

from serial_port_logger.models import LogFileModel

class LogFileSerializer(serializers.Serializer):
    device_name = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    file_name = serializers.CharField(
        read_only=True, max_length=100)
    file_path = serializers.CharField(
        read_only=True, max_length=100)

    def create(slef, validated_data):
        return LogFileModel.objects.create(validated_data)

    def update(self, instance, validated_data):
        # instance.delete()
        instance.device_name = validated_data.get(
            'device_name', instance.device_name)
        instance.save()
        return instance