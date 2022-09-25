from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('approve/', views.approve, name='Approve'),
    path('remove/', views.remove, name='Remove'),
    path('search/', views.search, name='Search'),
    path('facultyadd/', views.facultyAdd, name='Add'),
    path('facultyassign/', views.facultyAssign, name='Assign'),
]
