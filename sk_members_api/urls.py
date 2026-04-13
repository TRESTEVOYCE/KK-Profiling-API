from django.urls import path, include
from rest_framework import routers
from .views import MemberListCreate , MemberRetrieveUpdateDestroy

urlpatterns = [   
    path('members/', MemberListCreate.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberRetrieveUpdateDestroy.as_view(), name='member-retrieve-update-destroy'),
]