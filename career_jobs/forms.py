from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CareerJob


class CareerJobCreateForm(forms.ModelForm):
    job_title = forms.CharField(min_length=7)

    class Meta:
        model = CareerJob
        fields = (
            'job_title', 
            'company_name', 
            'job_location_country', 
            'job_location_city', 
            'job_type', 
            'job_description',
            'job_status',
            'tag',
        )
        labels = {
            'job_location_country': _('Country'),
            'job_location_city': _('City')
        }
