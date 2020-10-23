# django_telemetry_obd/admin.py
from django.contrib import admin
from .models import (
    VehicleManufacturer, VehicleModel, VehicleTrim, Vehicle,
    EcuDataFile, EcuData, EcuCommandStats
)

admin.site.site_header = "Telemetry OBD Django Server"

@admin.register(VehicleManufacturer)
class VehicleManufacturerAdmin(admin.ModelAdmin):
    fields = [
        "name",
    ]
    readonly_fields = ['id',  ]
    search_fields = ['name', ]


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    fields = [ 'vehicle_manufacturer', "name", ]
    readonly_fields = ['id',  ]
    search_fields = ['vehicle_manufacturer', 'name', ]


@admin.register(VehicleTrim)
class VehicleTrimAdmin(admin.ModelAdmin):
    fields = [ 'vehicle_model', "name", ]
    readonly_fields = ['id',  ]
    search_fields = ['vehicle_model', 'name', ]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    fields = [
        'vehicle_manufacturer', 'vehicle_model', 'vehicle_trim', 'vin', 'model_year',
        'is_manual_transmission', 'is_automatic_transmission', 'is_gas', 'is_diesel',
        'is_turbocharged', 'displacement', 'transmission_gears',
    ]
    readonly_fields = ['id',  'created', 'modified', ]
    search_fields = ['vehicle_manufacturer__name', 'vehicle_model__name', 'vehicle_trim__name', "vin", ]


@admin.register(EcuDataFile)
class EcuDataFileAdmin(admin.ModelAdmin):
    fields = [
        'vehicle', 'file_name', 'is_zipped',
        'first_iso_ts_pre', 'last_iso_ts_post', 'duration',
    ]
    readonly_fields = ['id', 'created', 'modified', ]
    search_fields = ['vehicle__vin', 'file_name', ]


@admin.register(EcuData)
class EcuDataAdmin(admin.ModelAdmin):
    fields = [
        'vehicle', 'ecu_data_file',
        'command_name', 'obd_response_value',
        'iso_ts_pre', 'iso_ts_post', 'duration',
    ]
    readonly_fields = ['id', ]
    search_fields = ['vehicle__vin', 'ecu_data_file__file_name', 'command_name', ]


@admin.register(EcuCommandStats)
class EcuCommandStatsticsAdmin(admin.ModelAdmin):
    fields = [
        'vehicle', 'command_name',
        'duration_average', 'duration_standard_deviation', 'duration_min', 'duration_max',
        'is_supported', 'is_pint_value', 'value_type',
        'value_average', 'value_standard_deviation', 'value_min', 'value_max',
        'records',
    ]
    readonly_fields = ['id', ]
    search_fields = ['vehicle__vin', 'command_name', ]


