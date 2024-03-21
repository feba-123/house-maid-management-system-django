from django import forms
from .models import Housemaid

class HousemaidStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Housemaid
        fields = ['status']