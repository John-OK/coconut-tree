from django.urls import path
from . import views

app_name = 'printful_integration'

urlpatterns = [
    path('create-order/', views.create_printful_order, name='create_printful_order'),
]
