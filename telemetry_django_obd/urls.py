# django_file_system_searcher/urls.py
from django.urls import path
from django.views.generic import TemplateView
from .views import (
    VehicleManufacturerViewSet,
    VehicleModelViewSet,
    VehicleTrimViewSet,
    VehicleViewSet,
    EcuDataFileViewSet,
    EcuDataViewSet,
    EcuCommandStatsViewSet,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name="telemetry_django_obd-index.html"), name='index'),

    path('vehicle_manufacturer/', VehicleManufacturerViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('vehicle_manufacturer/<int:pk>/', VehicleManufacturerViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('vehicle_model/', VehicleModelViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('vehicle_model/<int:pk>/', VehicleModelViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('vehicle_trim/', VehicleTrimViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('vehicle_trim/<int:pk>/', VehicleTrimViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('vehicle/', VehicleViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('vehicle/<int:pk>/', VehicleViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('ecu_data_file/', EcuDataFileViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('ecu_data_file/<int:pk>/', EcuDataFileViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('ecu_data/', EcuDataViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('ecu_data/<int:pk>/', EcuDataViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('ecu_command_stats/', EcuCommandStatsViewSet.as_view({
                                                'get': 'list', 'post': 'create'
                                            })
    ),
    path('ecu_command_stats/<int:pk>/', EcuCommandStatsViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
]


