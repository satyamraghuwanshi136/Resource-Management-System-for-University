from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('handle_model/', views.handleModel, name='HandleModel'),
]
