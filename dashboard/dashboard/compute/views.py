from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from . import models as m
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect
import logging
from .forms import ResourceCreateForm


User = get_user_model()


# Create your views here.
class ResourceListView(LoginRequiredMixin, ListView):
    model = (
        m.ComputeResource
    )  # .objects.select_related('network').filter(network__isnull=True)

    # def get_queryset(self):
    #     qs = (super(ResourceListView, self).get_queryset().all())
    #     logging.info("Printing qs")
    #     logging.info(qs)
    #           # prefetch_related('Network', 'NetworkOwner').filter(network__networkowner__owner=self.request.user))
    #     #logging.info("^^^^^^^^^^^^^^^^^")
    #     #logging.info(m.Network.objects.all().select_related('owners').filter(owners=self.request.user))
    #     return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResourceListView, self).get_context_data(**kwargs)
        #context["network"] = m.Network.objects.distinct()
        #context["network"] = m.Network.objects.all()
        context["network"] = m.Network.objects.select_related('owners').filter(owners=self.request.user)
        #logging.info(m.Network.objects.all().filter(owners=self.request.user).query)
            # .filter(owners=self.request.user)
        #logging.info("---------")
        #logging.info(context)
        return context


class NetworkCreateView(LoginRequiredMixin, CreateView):
    model = m.Network
    login_url = "login"
    fields = ("network_name", "network_description", "located_in_cloud")

    success_url = reverse_lazy("ComputeResources")

    def form_valid(self, form):
        form.instance.owners = self.request.user
        return super(NetworkCreateView,self).form_valid(form)




class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = m.ComputeResource
    form_class=ResourceCreateForm
    template_name='computeresource_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    #login_url = "login"
    # fields = (
    #      "network",
    #      "resource_name",
    #      "portable",
    #      "local_ipv4_address",
    #      "local_ipv6_address",
    #      "external_ipv4_address",
    #      "external_ipv6_address",
    #      "powered_on",
    #      "powered_on_utc",
    #      "uptime",
    #      "last_seen",
    #      "description",
    #  )
    # #form = PersonForm()
    success_url = reverse_lazy("ComputeResources")

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = m.ComputeResource
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# def networkResourceUpdate(request, id):
    # form_class = ResourceCreateView
    # model = m.ComputeResource
    # template_name = 'templates/computersource_form.html'

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.object = m.ComputeResource.objects.get(id=self.kwargs['id'])
    #
    # def get(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form_class(form_class)
    #     context = self.get_context_data(object=self.object, form=form)
    #     return self.render_to_response(context)
    # if request.method == 'POST':
    #     networkInstance =
    #     form = UserChangeForm(request.POST, instance=request.user)
    #
    #         if form.is_valid():
    #             form.save()
    #             return redirect('update-network-details', id=request.parse_context['kwargs']['id'])
    #
    # pass
