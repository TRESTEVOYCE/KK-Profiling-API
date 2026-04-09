from django.urls import path, include
from .views import EventListCreate, EventRetrieveUpdateDestroy

urlpatterns = [   
    path('', EventListCreate.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='event-retrieve-update-destroy'),
]

