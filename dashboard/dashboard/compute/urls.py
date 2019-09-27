from django.urls import path
from .views import ResourceListView, ResourceCreateView, NetworkCreateView, ResourceDetailView, NetworkResourceUpdate, NetworkResourceDelete\
                    , NetworkDetailView, NetworkUpdate, NetworkDelete


urlpatterns = [
     path('', ResourceListView.as_view(), name='ComputeResources'),
     path('create/', ResourceCreateView.as_view(), name='AddComputeResource'),
     path('add-network/', NetworkCreateView.as_view(), name='Add-Network'),
     path('<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
     path('<int:pk>/edit', NetworkResourceUpdate.as_view(), name='networkResource_edit'),
     path('<int:pk>/delete', NetworkResourceDelete.as_view(), name='networkResource_delete'),
     path('network/<int:pk>', NetworkDetailView.as_view(), name="network_detail"),
     path('network/<int:pk>/edit', NetworkUpdate.as_view(), name="network_edit"),
     path('network/<int:pk>/delete', NetworkDelete.as_view(), name="network_delete")
]
