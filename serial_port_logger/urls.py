from django.urls import path
from serial_port_logger import views

urlpatterns = [
    path('serial_ports/', views.serial_port_list),
    path('serial_ports/<str:device_name>', views.serial_port_detail),
]