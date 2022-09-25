from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.loginAuth, name='Login'),
    path('logout/', views.logoutAuth, name='Logout'),
]
