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
    path('profile/', views.profile, name='profile'),
#     path('forum/question/<int:question_id>/',views.question, name='question'),
]