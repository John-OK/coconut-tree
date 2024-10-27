from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    # path('get_mockup_result/<str:task_key>/', views.get_mockup_result, name='get_mockup_result'),
]