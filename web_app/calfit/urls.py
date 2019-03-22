from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('history/', views.history, name='history'),
    path('api/check_user/', views.api_check_user, name='api_check_user'),
    # path('api/get_user_notifications/', views.get_user_notifications, name='get user notifications')
]