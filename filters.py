from dataclasses import fields
import django_filters
from.models import *

class PredictionHistoryFilter(django_filters.FilterSet):
    class Meta:
        model = PredictionHistory
        fields = '__all__'
