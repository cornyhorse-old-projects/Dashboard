from django.contrib.auth import get_user_model
from .models import ComputeResource, Network
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import ResourceCreateForm, NetworkForm


User = get_user_model()


# Create your views here.
class ResourceListView(LoginRequiredMixin, ListView):
    model = ( ComputeResource )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResourceListView, self).get_context_data(**kwargs)
        context["network"] = Network.objects.select_related('owners').filter(owners=self.request.user)
        return context


class NetworkCreateView(LoginRequiredMixin, CreateView):
    model = Network
    login_url = "login"
    form_class = NetworkForm

    success_url = reverse_lazy("networkResources")

    def form_valid(self, form):
        form.instance.owners = self.request.user
        return super(NetworkCreateView, self).form_valid(form)


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = ComputeResource
    form_class = ResourceCreateForm
    template_name = 'computeresource_form.html'
    success_url = reverse_lazy("networkResources")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = ComputeResource
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NetworkResourceUpdate(LoginRequiredMixin, UpdateView):
    model = ComputeResource
    form_class = ResourceCreateForm
    template_name = 'compute/computeresource_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('resource_detail', pk=self.kwargs['pk'])


class NetworkResourceDelete(LoginRequiredMixin, DeleteView):
    model = ComputeResource
    success_url = reverse_lazy('networkResources')
    template_name = 'compute/resource_delete.html'


class NetworkDetailView(LoginRequiredMixin, DetailView):
    model = Network
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NetworkUpdate(LoginRequiredMixin, UpdateView):
    model = Network
    form_class = NetworkForm
    template_name = 'compute/network_update.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('network_detail', pk=self.kwargs['pk'])


class NetworkDelete(LoginRequiredMixin, DeleteView):
    model = Network
    success_url = reverse_lazy('networkResources')
    template_name = 'compute/resource_delete.html'
