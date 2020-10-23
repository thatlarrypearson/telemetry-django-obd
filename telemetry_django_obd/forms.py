from django.forms import ModelForm
from .models import EcuData
 
class EcuDataForm(ModelForm):
    class Meta:
        model = EcuData
        fields = ['vehicle', 'ecu_data_file', 'command_name', 'obd_response_value',
                    'iso_ts_pre', 'iso_ts_post', 'duration',
                ]
