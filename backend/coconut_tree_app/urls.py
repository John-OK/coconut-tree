from django.urls import path
from . import views

app_name = 'coconut_tree_app'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user_answer', views.user_answer, name='user_answer'),
]