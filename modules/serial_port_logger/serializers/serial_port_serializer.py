from rest_framework import serializers

from serial_port_logger.models import SerialPortConfigModel

class SerialPortSerializer(serializers.Serializer):
    device_name = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    log_file = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    driver = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    baud_rate = serializers.ChoiceField(
        choices=SerialPortConfigModel.baud_rate_choices, required=True)
    flow_control = serializers.ChoiceField(
        choices=SerialPortConfigModel.flow_control_choices, required=True)
    parity = serializers.ChoiceField(
        choices=SerialPortConfigModel.parity_choices, required=True)
    stop_bits = serializers.ChoiceField(
        choices=SerialPortConfigModel.stop_bits_choices, required=True)
    character_size = serializers.IntegerField(required=True)

    def create(slef, validated_data):
        return SerialPortConfigModel.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.delete()
        instance.device_name = validated_data.get(
            'device_name', instance.device_name)
        instance.log_file = validated_data.get('log_file', instance.log_file)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.baud_rate = validated_data.get('baud_rate', instance.baud_rate)
        instance.flow_control = validated_data.get(
            'flow_control', instance.flow_control)
        instance.parity = validated_data.get('parity', instance.parity)
        instance.stop_bits = validated_data.get('stop_bits', instance.stop_bits)
        instance.character_size = validated_data.get(
            'character_size', instance.character_size)
        instance.save()
        return instance