from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from . import models as m
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

User = get_user_model()

# Create your views here.
class ResourceListView(LoginRequiredMixin, ListView):
    model = (
        m.ComputeResource
    )  # .objects.select_related('network').filter(network__isnull=True)

    def get_queryset(self):
        qs = (
            super(ResourceListView, self).get_queryset().filter(owner=self.request.user)
        )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResourceListView, self).get_context_data(**kwargs)
        context["network"] = m.Network.objects.distinct()
        return context


class NetworkCreateView(LoginRequiredMixin, CreateView):
    model = m.Network
    login_url = "login"
    fields = ("network_name", "network_description", "located_in_cloud")
    success_url = reverse_lazy("ComputeResources")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = m.ComputeResource
    login_url = "login"
    fields = (
        "network",
        "resource_name",
        "portable",
        "local_ipv4_address",
        "local_ipv6_address",
        "external_ipv4_address",
        "external_ipv6_address",
        "powered_on",
        "powered_on_utc",
        "uptime",
        "last_seen",
        "description",
    )
    success_url = reverse_lazy("ComputeResources")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = m.ComputeResource
    login_url = 'login'
