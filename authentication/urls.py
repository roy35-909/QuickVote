
from django.urls import path
from authentication.views import *
urlpatterns = [

    path('registration', registration),
    path('registration/<int:fid>', finger_register.as_view()),
    path('login', login),
    path('logout', logout),
    path('login/<str:email>', finger_login.as_view()),
]
