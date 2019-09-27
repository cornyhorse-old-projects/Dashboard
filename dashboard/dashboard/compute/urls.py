from django.urls import path
from .views import ResourceListView, ResourceCreateView, NetworkCreateView, ResourceDetailView, NetworkResourceUpdate


urlpatterns = [
     path('', ResourceListView.as_view(), name='ComputeResources'),
     path('create/', ResourceCreateView.as_view(), name='AddComputeResource'),
     path('add-network/', NetworkCreateView.as_view(), name='Add-Network'),
     path('<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
     path('<int:pk>/edit', NetworkResourceUpdate.as_view(), name='networkResource_edit'),
]
