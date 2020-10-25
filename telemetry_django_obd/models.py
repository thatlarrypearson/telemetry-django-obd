# django_telemetry_obd/models.py
from django.db import models


class VehicleManufacturer(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(unique=True, db_index=True, verbose_name='Name', max_length=128)

    def __str__(self):
        return f"{self.id}, {self.name}"


class VehicleModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    vehicle_manufacturer = models.ForeignKey(VehicleManufacturer, on_delete=models.PROTECT, verbose_name='Manufacturer')
    name = models.CharField(verbose_name='Name', max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vehicle_manufacturer', 'name', ], name='vehicle_manufacturer_model_name_vehicle_model'
            ),
        ]

    def __str__(self):
        return f"{self.id}, {self.vehicle_manufacturer.name}, {self.name}"


class VehicleTrim(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT, verbose_name='Model')
    name = models.CharField(verbose_name='Name', max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vehicle_model', 'name', ], name='vehicle_model_trim_name_vehicle_trim'
            ),
        ]

    def __str__(self):
        return f"{self.id}, {self.vehicle_model.vehicle_manufacturer.name}, {self.vehicle_model.name}, {self.name}"


class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    vehicle_manufacturer = models.ForeignKey(
        VehicleManufacturer, on_delete=models.PROTECT, verbose_name='Manufacturer',
        null=True, default=None
    )
    vehicle_model = models.ForeignKey(
        VehicleModel, on_delete=models.PROTECT, verbose_name='Model',
        null=True, default=None
    )
    vehicle_trim = models.ForeignKey(
        VehicleTrim, on_delete=models.PROTECT, verbose_name='Trim',
        null=True, default=None
    )
    vin = models.CharField(unique=True, db_index=True, verbose_name='VIN', max_length=32)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')
    model_year = models.IntegerField(default=0, verbose_name='Model Year')
    is_manual_transmission = models.BooleanField(default=False, verbose_name='Is Manual Transmission')
    is_automatic_transmission = models.BooleanField(default=False, verbose_name='Is Automatic Transmission')
    is_gas = models.BooleanField(default=False, verbose_name='Is Gas')
    is_diesel = models.BooleanField(default=False, verbose_name='Is Diesel')
    is_turbocharged = models.BooleanField(default=False, verbose_name='Is Turbocharged')
    displacement = models.CharField(default='', blank=True, verbose_name='Displacement', max_length=64)
    transmission_gears = models.IntegerField(default=0, verbose_name='Transmission Gears')

    def __str__(self):
        s = ''
        if self.vehicle_manufacturer:
            s = f", {self.vehicle_manufacturer.name}"
        if self.vehicle_model:
            s += f", {self.vehicle_model.name}"

        return f"{self.id}{s}, {self.vin}"


class EcuDataFile(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vehicle')
    file_name = models.CharField(unique=True, db_index=True, verbose_name='File Name', max_length=512)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')
    is_zipped = models.BooleanField(default=False, verbose_name='Is Zipped')
    first_iso_ts_pre = models.DateTimeField(null=True, verbose_name='First Timestamp')
    last_iso_ts_post = models.DateTimeField(null=True, verbose_name='Last Timestap')
    duration = models.DurationField(verbose_name='Duration', null=True, default=None)
    records = models.IntegerField(default=0, verbose_name='Records')

    def __str__(self):
        return f"{self.id}, {self.vehicle.vin}, {self.file_name}"


class EcuData(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vehicle')
    ecu_data_file = models.ForeignKey(EcuDataFile, on_delete=models.PROTECT, verbose_name="ECU Data File")
    command_name = models.CharField(verbose_name='Command Name', max_length=128)
    obd_response_value = models.CharField(verbose_name='OBD Response Value', max_length=512)
    iso_ts_pre = models.DateTimeField(verbose_name='Timestamp Before')
    iso_ts_post = models.DateTimeField(verbose_name='Timestamp After')
    duration = models.DurationField(verbose_name='Duration')

    class Meta:
        verbose_name_plural = 'ECU Data'


    def __str__(self):
        return f"{self.id}, {self.vehicle.vin}, {self.ecu_data_file.file_name}, {self.command_name}"


class EcuCommandStats(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vehicle')
    command_name = models.CharField(verbose_name='Command_name', max_length=128)
    duration_average = models.DurationField(verbose_name='Duration Average', null=True, default=None)
    duration_standard_deviation = models.DurationField(verbose_name='Duration Standard Deviation', null=True, default=None)
    duration_min = models.DurationField(verbose_name='Duration Minimum', null=True, default=None)
    duration_max = models.DurationField(verbose_name='Duration Maximum', null=True, default=None)
    is_supported = models.BooleanField(default=False, verbose_name='Is Supported')
    is_pint_value = models.BooleanField(default=False, verbose_name='Is Pint Value')
    value_type = models.CharField(default='', verbose_name='Value Type', blank=True, max_length=512)
    value_average = models.FloatField(default=0.0, verbose_name='Value Average')
    value_standard_deviation = models.FloatField(default=0.0, verbose_name='Value Standard Deviation')
    value_min = models.FloatField(default=0.0, verbose_name='Value Minimum')
    value_max = models.FloatField(default=0.0, verbose_name='Value Maximum')
    records = models.IntegerField(default=0, verbose_name='Records')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vehicle', 'command_name', ], name='v_cmd_name_ecu_cmd_stats'
            ),
        ]
        verbose_name_plural = 'ECU Command Stats'

    def __str__(self):
        return f"{self.id}, {self.vehicle.vin}, {self.command_name}"
