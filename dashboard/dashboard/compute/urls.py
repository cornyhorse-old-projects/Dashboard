from django.urls import path
from .views import ResourceListView, ResourceCreateView, NetworkCreateView, ResourceDetailView, NetworkResourceUpdate, NetworkResourceDelete\
                    , NetworkDetailView, NetworkUpdate, NetworkDelete


urlpatterns = [
     path('', ResourceListView.as_view(), name='networkResources'),
     path('create/', ResourceCreateView.as_view(), name='add_networkResource'),
     path('add-network/', NetworkCreateView.as_view(), name='add_network'),
     path('<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
     path('<int:pk>/update', NetworkResourceUpdate.as_view(), name='networkResource_update'),
     path('<int:pk>/delete', NetworkResourceDelete.as_view(), name='networkResource_delete'),
     path('network/<int:pk>', NetworkDetailView.as_view(), name="network_detail"),
     path('network/<int:pk>/update', NetworkUpdate.as_view(), name="network_update"),
     path('network/<int:pk>/delete', NetworkDelete.as_view(), name="network_delete")
]
