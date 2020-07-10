from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from serial_port_logger.models import SerialPortConfigModel
from serial_port_logger.models import RecordingModel
from serial_port_logger.serializers import SerialPortSerializer
from serial_port_logger.serializers import RecordingSerializer

@csrf_exempt
def serial_port_list(request):
    if request.method == 'GET':
        devices = SerialPortConfigModel.objects.all()
        serializer = SerialPortSerializer(devices, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SerialPortSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def serial_port_detail(request, device_name):
    device = SerialPortConfigModel.objects.get(device_name)
    if device == None:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = SerialPortSerializer(device)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SerialPortSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        device.delete()
        return HttpResponse(status=204)

@csrf_exempt
def recording(request):
    recording = RecordingModel.get()
    if recording == None:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RecordingSerializer(recording)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RecordingSerializer(recording, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)