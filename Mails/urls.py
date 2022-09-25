from django.urls import include, path
from . import views

urlpatterns = [
    path('compose/', views.compose, name='Compose'),
    path('bulk/', views.bulk, name='Bulk'),
    path('smssend/', views.smsSend, name='SendSMS'),
]
