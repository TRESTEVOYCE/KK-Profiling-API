from django.urls import path
from .views import  filter_youth_profiles, home_view, login_view, logout_view, search_youth_profiles, youth_profile_view ,events_view, settings_view, organization_view, event_detail_view,add_event_view,create_youth_profile_view,update_position_view,edit_youth_profile_view,delete_youth_profile_view
from kkSystem import views

urlpatterns = [
    path('', login_view, name='loginn'),
    path('logoutt/', logout_view, name='logoutt'),
    path('home/', home_view, name='home'),
    path('youth-profile/', youth_profile_view, name='youth-profile'),
    path('search/', search_youth_profiles, name='search_youth_profiles'),
    path('filter/', filter_youth_profiles, name='filter_youth_profiles'), 
    path('youth-profiles/', youth_profile_view, name='youth-profiles'),
    path('create-youth/', create_youth_profile_view, name='add_youth'), 
    path('events/', events_view, name='events'),
    path('events/<int:event_id>/', event_detail_view, name='view_events'),
    path('settings/', settings_view, name='settings'),
    path('organization/', organization_view, name='organization'),
    path('events/add/', add_event_view, name='add_event'),
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail_view'),
    path('members/update/<str:role>/', views.update_position_view, name='update_position_view'),
    path('edit-youth/<int:profile_id>/', views.edit_youth_profile_view, name='edit_youth_profile_view'),
    path('delete-youth/<int:profile_id>/', views.delete_youth_profile_view, name='delete_youth_profile_view'),
]