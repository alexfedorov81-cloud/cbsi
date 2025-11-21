from django import forms
from .models import CallbackRequest


class CallbackForm(forms.ModelForm):
    service_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone', 'service']
        widgets = {
            'service': forms.HiddenInput(),  # Скрытое поле для услуги
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['phone'].required = True