# https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/
import json
from dateutil import parser
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError, OperationalError
from ...models import EcuData, EcuDataFile, Vehicle
from ...forms import EcuDataForm


class Command(BaseCommand):
    help = 'Loads OBD/ECU data created by telemetry-obd'

    def get_vin_from_file_name(self, file_name) -> str:
        path = str((Path(file_name)).name)

        file_name_parts = path.split('-')
        return file_name_parts[0]

    def get_vehicle_from_file_name(self, file_name) -> Vehicle:
        vin = self.get_vin_from_file_name(file_name)
        path = Path(file_name)
        if not path.is_file():
            raise ValueError

        try:
            vehicle = Vehicle.objects.get(vin=vin)
        except Vehicle.DoesNotExist:
            vehicle = Vehicle()
            vehicle.vin = vin
            vehicle.save()
        return vehicle

    def get_ecu_data_file_from(self, vehicle, file_name) -> EcuDataFile:
        try:
            ecu_data_file = EcuDataFile.objects.get(file_name=str((Path(file_name)).name))
            return None
        except:
            ecu_data_file = EcuDataFile()
            ecu_data_file.vehicle = vehicle
            ecu_data_file.file_name = str((Path(file_name)).name)
            ecu_data_file.save()
        return ecu_data_file

    def add_arguments(self, parser):
        parser.add_argument(
                "file_names",
                nargs='*',
                metavar="file_names",
                help="Relative or absolute file path(s)."
            )

    def handle(self, *args, **options):
        for file_name in options['file_names']:
            vehicle = self.get_vehicle_from_file_name(file_name)
            ecu_data_file = self.get_ecu_data_file_from(vehicle, file_name)
            if not ecu_data_file:
                print(f"{file_name}: already processed, skipping...")
                continue

            first_iso_ts_pre = None
            last_iso_ts_post = None
            records = 0

            with open(file_name, "r") as file:
                print(f"{file_name}: processing")
                for line in file:
                    records += 1
                    try:
                        record = json.loads(line)
                    except json.decoder.JSONDecodeError as e:
                        print(str(e))
                        print(f"Record: {records} JSONDecodeError")
                        break

                    record['vehicle'] = vehicle
                    record['ecu_data_file'] = ecu_data_file

                    record['iso_ts_pre'] = parser.isoparse(record['iso_ts_pre'])
                    record['iso_ts_post'] = parser.isoparse(record['iso_ts_post'])
                    record['duration'] = record['iso_ts_post'] - record['iso_ts_pre']

                    form = EcuDataForm(record)

                    if form.is_valid():
                        ecu_data = form.save(commit=False)
                        ecu_data.duration = ecu_data.iso_ts_post - ecu_data.iso_ts_pre
 
                        try:
                            ecu_data.save()

                            if not first_iso_ts_pre:
                                first_iso_ts_pre = ecu_data.iso_ts_pre
                            last_iso_ts_post = ecu_data.iso_ts_post

                        except (OperationalError, DataError) as e:
                            print('\n', e, '\n', record, '\n')
                    else:
                        print('\n', form.errors, '\n', record, '\n')

                        
                ecu_data_file.first_iso_ts_pre = first_iso_ts_pre
                ecu_data_file.last_iso_ts_post = last_iso_ts_post
                ecu_data_file.duration = last_iso_ts_post - first_iso_ts_pre
                ecu_data_file.records = records

                ecu_data_file.save()


