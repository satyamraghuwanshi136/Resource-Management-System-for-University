from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.dashboard, name='Dashboard'),
    path('profile/', views.profile, name='Profile'),
    path('apiprofile/', views.apiProfile, name='APIProfile'),
    path('permissionform/', views.permissionForm, name='PermissionForm'),
    path('setup/', views.setup, name='Setup'),
    path('verification/', views.verification, name='Verification'),
    path('apitwilioprofile/', views.twilioAPI, name='APITwilioProfile'),
    path('checkenroll/', views.checkEnroll, name='CheckEnroll'),
    path('checkemployee/', views.checkEmployee, name='CheckEmployee'),
    path('updatestudent/', views.updateStudent, name='UpdateStudent'),
    path('updatefaculty/', views.updateFaculty, name='UpdateFaculty'),
    path('inventory_manage/', views.Inventory_Manage, name='Inventory_Manage'),
]

