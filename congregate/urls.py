from django.urls import path
from . import views

urlpatterns = [
    path('', views.testview, name='test'),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('register', views.new_user, name='registration'),
    path('<slug:username>/home/', views.UserHome.as_view(), name='home'),
    path('<slug:username>/groups/', views.UserGroup.as_view(), name='user_groups'),
    path('group/<int:group_id>', views.GroupHome.as_view(), name='group_home'),
    path('new/event/', views.new_event, name='new_event'),
    path('event/<int:event_id>', views.EventHome.as_view(), name='event_home'),
    path('add-user-group/', views.add_user_group, name='add_user_group'),
    path('new/activity/', views.new_activity, name='new_event'),
]
