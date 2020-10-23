# django_file_system_searcher/view.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import django_filters.rest_framework
from .models import (
    VehicleManufacturer, VehicleModel, VehicleTrim, Vehicle,
    EcuDataFile, EcuData, EcuCommandStats
)
from .serializers import (
    VehicleManufacturerSerializer, VehicleModelSerializer,
    VehicleTrimSerializer, VehicleSerializer,
    EcuDataFileSerializer, EcuDataSerializer, EcuCommandStatsSerializer
)


class VehicleManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleManufacturerSerializer
    model = VehicleManufacturer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['name', ]
    queryset = VehicleManufacturer.objects.all()


class VehicleModelViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleModelSerializer
    model = VehicleModel
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['name', 'vehicle_manufacturer__name',]
    queryset = VehicleModel.objects.all()


class VehicleTrimViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleTrimSerializer
    model = VehicleTrim
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['name', 'vehicle_model__name', ]
    queryset = VehicleTrim.objects.all()


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    model = Vehicle
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = [
        'vin', 
        'vehicle_trim__name', 'vehicle_model__name', 'vehicle_manufacturer__name',
    ]
    queryset = Vehicle.objects.all()


class EcuDataFileViewSet(viewsets.ModelViewSet):
    serializer_class = EcuDataFileSerializer
    model = EcuDataFile
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = [ 'file_name', 'vehicle__vin', ]
    queryset = EcuDataFile.objects.all()


class EcuDataViewSet(viewsets.ModelViewSet):
    serializer_class = EcuDataSerializer
    model = EcuData
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = [ 'ecu_data_file__file_name', 'vehicle__vin', ]
    queryset = EcuData.objects.all()


class EcuCommandStatsViewSet(viewsets.ModelViewSet):
    serializer_class = EcuCommandStatsSerializer
    model = EcuCommandStats
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = [ 'command_name', 'vehicle__vin', ]
    queryset = EcuCommandStats.objects.all()


