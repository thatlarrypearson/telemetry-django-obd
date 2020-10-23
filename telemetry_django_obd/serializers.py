# django_file_system_searcher/serializers.py
from rest_framework import serializers
from .models import (
    VehicleManufacturer, VehicleModel, VehicleTrim, Vehicle,
    EcuDataFile, EcuData, EcuCommandStats
)


class VehicleManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleManufacturer
        fields = [ 'id', 'name', ]


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = [ 'id', 'vehicle_manufacturer', 'name', ]


class VehicleTrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTrim
        fields = [ 'id', 'vehicle_model', 'name', ]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id', 'vehicle_manufacturer', 'vehicle_model', 'vehicle_trim',
            'vin', 'model_year', 'displacement',
            'is_manual_transmission', 'is_automatic_transmission',
            'transmission_gears',
            'is_gas', 'is_diesel',
            'is_turbocharged',
        ]
        read_only = ['created', 'modified', ]


class EcuDataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcuDataFile
        fields = [
            'id', 'vehicle', 'file_name', 'is_zipped',
            'first_iso_ts_pre', 'last_iso_ts_post',
            'duration', 'records',
        ]
        read_only = ['created', 'modified', ]


class EcuDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcuData
        fields = [
            'id', 'vehicle', 'ecu_data_file',
            'command_name', 'obd_response_value',
            'iso_ts_pre', 'iso_ts_post', 'duration',
        ]


class EcuCommandStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcuCommandStats
        fields = [
            'id', 'vehicle', 'command_name',
            'duration_average', 'duration_standard_deviation',
            'duration_min', 'duration_max',
            'is_supported', 'is_pint_value',
            'value_average', 'value_standard_deviation',
            'value_min', 'value_max',
            'records',
        ]


