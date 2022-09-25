from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('cwtake/', views.cwTake, name='CWTake'),
    path('cwtakeupdate/', views.cwTakeUpdate, name='CWTakeUpdate'),
    path('cwviewstudent/', views.cwViewStudent, name='CWViewStudent'),
    path('swtake/', views.swTake, name='SWTake'),
    path('swtakeupdate/', views.swTakeUpdate, name='SWTakeUpdate'),
    path('swviewstudent/', views.swViewStudent, name='SWViewStudent'),
    path('viewmarks/', views.viewMarks, name='ViewMarks'),
    path('viewmarksexport/', views.viewMarksExport, name='ViewMarksExport'),
    path('viewchart/', views.chartView, name='Chart'),
    path('swviewchart/', views.swChartView, name='SWChart'),
]