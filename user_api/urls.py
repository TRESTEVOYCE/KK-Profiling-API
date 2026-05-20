from django.urls import path, include
from .views import (
    LoginView, 
    LogoutView, 
    UserListCreateView, 
    UserDeleteView # Changed to match the DestroyAPIView
)

urlpatterns = [
    # Auth Endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
]

