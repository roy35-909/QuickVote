
from django.urls import path
from .views import *
urlpatterns = [

    path('', home),
    path('vote/<int:pk>', select_vote),
    path('vote/make_vote/<int:pk>', make_vote),
    path('vote/give_vote/<int:pk>', give_vote),
    path('vote/become_candidate/<int:pk>', become_candidate),

]
