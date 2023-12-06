from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('active_account/<str:uidb64>/<str:token>', active_account, name='active_account'),
    path('home/', home, name='home'),
]
