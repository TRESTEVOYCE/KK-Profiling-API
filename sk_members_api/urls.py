from django.urls import path, include
from rest_framework import routers
from sk_members_api import views



router = routers.DefaultRouter()
router.register(r'members', views.MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]