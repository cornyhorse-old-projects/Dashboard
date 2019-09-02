from django.urls import path
from .views import ResourceListView, ResourceCreateView


urlpatterns = [
    path('', ResourceListView.as_view(), name='ComputeResources'),
    path('create/', ResourceCreateView.as_view(), name='AddComputeResource')
]
