from django.urls import path, include
from .views import KKAddressViewSet, ProfilingInformationsViewSet, ProfilingInformationsDetailViewSet, YouthStatusViewSet, YouthStatusDetailViewSet, KKAddressDetailViewSet

urlpatterns = [
    path('profiling-informations/', ProfilingInformationsViewSet.as_view(), name='profiling-informations-list-create'),
    path('profiling-informations/<int:pk>/', ProfilingInformationsDetailViewSet.as_view(), name='profiling-informations-retrieve-update-destroy'),
    path('kk-address/', KKAddressViewSet.as_view(), name='kk-address-list-create'),
    path('kk-address/<int:pk>/', KKAddressDetailViewSet.as_view(), name='kk-address-retrieve-update-destroy'),
    path('youth-status/', YouthStatusViewSet.as_view(), name='youth-status-list-create'),
    path('youth-status/<int:pk>/', YouthStatusDetailViewSet.as_view(), name='youth-status-retrieve-update-destroy'),
]