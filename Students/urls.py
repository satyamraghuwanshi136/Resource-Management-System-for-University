from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('search/', views.search, name='Search'),
    path('remove/', views.remove, name='Remove'),
    path('studentadd/', views.studentAdd, name='Add'),
    path('changesemester/', views.changeSemester, name='ChangeSemester'),
]
