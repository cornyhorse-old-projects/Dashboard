from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Network,ComputeResource


class ResourceCreateForm(forms.ModelForm):
    class Meta:
        model = ComputeResource
        fields = ["network", "resource_name", "portable", "local_ipv4_address", "local_ipv6_address",
        "external_ipv4_address", "external_ipv6_address", "powered_on", "powered_on_utc", "uptime",
        "last_seen", "description"]



    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['network'].queryset = self.fields['network'].queryset.filter(
            owners=user)

class NetworkForm(forms.ModelForm):

    class Meta:
        model = Network
        fields = ["network_name", "network_description", "located_in_cloud"]
