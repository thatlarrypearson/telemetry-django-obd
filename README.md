# UNDER CONSTRUCTION - Telemetry Django OBD Application

This [Django](https://www.djangoproject.com/) application contains two [Custom Management Commandds](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/) to:

- Load OBD/ECU data created by telemetry-obd into a database.
- Calculates simple statistics for each OBD command by VIN and places that data into the database.

## ```load_obd_data_files```

The Django management program, ```load_obd_data_files```, loads data created by [Telemetry OBD Logging/telemetry-obd](https://github.com/thatlarrypearson/telemetry-obd) into a database.

### USAGE

```python
python3.8 manage.py load_obd_data_files
```

## ```ecu_command_stats.py```

### USAGE

```python
python3.8 manage.py ecu_command_stats.py
```

## Installation

```bash
python3.8 -m pip install pip --upgrade
python3.8 -m pip install setuptools --upgrade
python3.8 -m pip install wheel --upgrade
git clone https://github.com/thatlarrypearson/telemetry-django-obd.git
cd telemetry-django-obd
python3.8 setup.py sdist
python3.8 -m pip install .
```

### Check Installation

