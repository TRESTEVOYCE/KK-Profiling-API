from django.urls import path
from .views import LoginView, LogoutView, UserListCreate, UserRetrieveUpdateDestroy


urlpatterns = [    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-retrieve-update-destroy'),

]