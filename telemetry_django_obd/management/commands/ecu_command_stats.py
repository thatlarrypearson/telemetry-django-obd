# https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/
import pint
from datetime import timedelta
from math import sqrt
from django.core.management.base import BaseCommand
from django.db.utils import DataError, OperationalError, NotSupportedError
from django.db.models import Avg, StdDev, Max, Min
from ...models import Vehicle, EcuData, EcuCommandStats


# Algorithms for calculating variance - Use Welford's Online Algorithm
# https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance

# An example Python implementation for Welford's algorithm is given below.
#
# For a new value newValue, compute the new count, new mean, the new M2.
# mean accumulates the mean of the entire dataset
# M2 aggregates the squared distance from the mean
# count aggregates the number of samples seen so far
class Welford():
    existing_aggregate = (0, 0.0, 0.0)

    def __init__(self):
        pass

    def update(self, newValue):
        (count, mean, M2) = self.existing_aggregate
        count += 1
        delta = newValue - mean
        mean += delta / count
        delta2 = newValue - mean
        M2 += delta * delta2
        self.existing_aggregate = (count, mean, M2)

    # Retrieve the mean, variance and sample variance from an aggregate
    def finalize(self):
        (count, mean, M2) = self.existing_aggregate
        if count < 2:
            raise ValueError("Welford's algorithm fails with less than 2 samples.")
        else:
            (mean, variance, sampleVariance) = (mean, M2 / count, M2 / (count - 1))
            return (mean, variance, sampleVariance)


class Command(BaseCommand):
    help = 'Calculate simple statistics for each OBD command issued to one or more VINs.'

    def add_arguments(self, parser):
        parser.add_argument(
                "vins",
                nargs='*',
                metavar="vins",
                default=[],
                help="One or more VINs.  Default is all VINs."
            )

    def handle(self, *args, **options):
        if isinstance(options['vins'], list):
            if not options['vins']:
                vehicles = Vehicle.objects.all()
            else:
                vehicles = Vehicle.objects.filter(vin__in=options['vins'])
        else:
            raise ValueError('missing VINs')

        unit_registry = pint.UnitRegistry()

        for vehicle in vehicles:

            print(f"{vehicle.__str__()}")

            ecu_command_stats = {}
            pint_max = {}
            pint_min = {}
            pint_units = {}
            duration_max = {}
            duration_min = {}
            records = {}
            pint_welford = {}
            duration_welford = {}

            for record in EcuData.objects.filter(vehicle=vehicle).all():
                command_name = record.command_name

                if command_name not in ecu_command_stats:
                    try:
                        ecu_command_stats[command_name] = EcuCommandStats.objects.get(vehicle=vehicle, command_name=command_name)
                    except EcuCommandStats.DoesNotExist:
                        ecu_command_stats[command_name] = EcuCommandStats(vehicle=vehicle, command_name=command_name)

                    # Algorithms for calculating variance - Use Welford's Online Algorithm
                    # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
                    pint_welford[command_name] = Welford()
                    duration_welford[command_name] = Welford()

                    pint_max[command_name] = None
                    pint_min[command_name] = None
                    duration_max[command_name] = None
                    duration_min[command_name] = None
                    records[command_name] = 0

                if record.obd_response_value != 'not supported':
                    ecu_command_stats[command_name].is_supported = True

                # Welford doesn't take kindly to timedelta arithmetic - convert to microseconds
                duration_welford[command_name].update(record.duration / timedelta(microseconds=1))

                if not duration_min[command_name] or duration_min[command_name] > record.duration:
                    duration_min[command_name] = record.duration
                    
                if not duration_max[command_name] or record.duration > duration_max[command_name]:
                    duration_max[command_name] = record.duration

                records[command_name] += 1

                try:
                    # some values may not be pint values
                    pint_value = unit_registry(record.obd_response_value)
                except:
                    continue

                pint_welford[command_name].update(pint_value.magnitude)

                if not pint_min[command_name] or pint_min[command_name] > pint_value:
                    pint_min[command_name] = pint_value

                if not pint_max[command_name] or pint_value > pint_max[command_name]:
                    pint_max[command_name] = pint_value

                ecu_command_stats[command_name].is_pint_value = True

            for command_name in ecu_command_stats:
                ecu_command_stats[command_name].records = records[command_name]

                ecu_command_stats[command_name].duration_max = duration_max[command_name]
                ecu_command_stats[command_name].duration_min = duration_min[command_name]

                try:
                    # Welford doesn't take kindly to timedelta arithmetic - microseconds back to timedelta
                    mean, variance, sample_variance = duration_welford[command_name].finalize()
                    ecu_command_stats[command_name].duration_average = timedelta(
                        milliseconds=int(mean)
                    )
                    ecu_command_stats[command_name].duration_standard_deviation = timedelta(
                        milliseconds=int(sqrt(variance))
                    )
                except ValueError:
                    print(f"{vehicle.vin}, {command_name} duration welford failed.")

                if pint_max[command_name]:
                    ecu_command_stats[command_name].value_max = pint_max[command_name].magnitude
                    ecu_command_stats[command_name].value_min = pint_min[command_name].magnitude
                    ecu_command_stats[command_name].value_type = pint_max[command_name].units.__str__()
                else:
                    ecu_command_stats[command_name].value_max = 0.0
                    ecu_command_stats[command_name].value_min = 0.0
                    ecu_command_stats[command_name].pint_units = ''

                try:
                    mean, variance, sample_variance = pint_welford[command_name].finalize()
                    ecu_command_stats[command_name].value_average = mean
                    ecu_command_stats[command_name].value_standard_deviation = sqrt(variance)
                except ValueError:
                    ecu_command_stats[command_name].value_average = 0.0
                    ecu_command_stats[command_name].value_standard_deviation = 0.0
                    print(f"{vehicle.vin}, {command_name} pint welford failed.")


                ecu_command_stats[command_name].save()


