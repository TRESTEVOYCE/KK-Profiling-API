from django.urls import path, include
from rest_framework import routers

from events_api.views import EventListCreate, EventRetrieveUpdateDestroy
from .views import MemberListCreate , MemberRetrieveUpdateDestroy

urlpatterns = [   
    path('', EventListCreate.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='event-retrieve-update-destroy'),
    path('members/', MemberListCreate.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberRetrieveUpdateDestroy.as_view(), name='member-retrieve-update-destroy'),
]