from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('viewattendance/', views.viewAttendance, name='ViewAttendance'),
    path('take/', views.take, name='Take'),
    path('takesuccess/', views.takeSuccess, name='TakeSuccess'),
    path('report/', views.generateReport, name='Generate'),
    path('viewattendancestudents/', views.viewAttendanceStudent, name='ViewStudent'),
    path('multiple/', views.multiple, name='Multiple'),
    path('checkmultiple/', views.checkMultiple, name='CheckMultiple'),
    path('updateattendance/', views.updateAttendance, name='UpdateAttendance'),
]
