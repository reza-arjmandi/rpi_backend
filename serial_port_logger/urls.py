from django.urls import path
from serial_port_logger import views

urlpatterns = [
    path('serial_ports/', views.serial_port_list, name='serial_port_list'),
    path('serial_ports/<str:device_name>/', views.serial_port_detail, 
        name='serial_port_detail'),
    path('recording/', views.recording, name='recording'),
    path('log_file/', views.log_file_list, name='log_file_list'),
    path('log_file/<str:device_name>/', views.log_file_detail, name='log_file_detail'),
    path('log_file/<str:device_name>/content/', views.log_file_content, name='log_file_content'),
]