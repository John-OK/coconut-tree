from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_the_homepage),
    path('user_answer', views.user_answer),
]