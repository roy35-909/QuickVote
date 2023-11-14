
from django.urls import path
from .views import *
urlpatterns = [

    path('', dashboard),
    path('candidate', candidate),
    path('candidate/make_delete/<int:pk>', make_candidate_delete),
    path('candidate/make_accept/<int:pk>', make_candidate_accept),
    path('vote', dashboard_vote),
    path('vote/make_start/<int:pk>', make_start_vote),
    path('vote/make_done/<int:pk>', make_vote_done),
    path('vote/make_delete/<int:pk>', make_vote_delete),
    path('show_result', show_result),


]
