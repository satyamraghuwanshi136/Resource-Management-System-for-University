from django.urls import include, path
from . import views


urlpatterns = [
    path('course/', views.course, name='Course'),
    path('branch/', views.branch, name='Branch'),
    path('semester/', views.semester, name='Semester'),
    path('subject/', views.subject, name='Subject'),
	path('400/<str:exception>', views.handler400, name='Error400'),
	path('403/<str:exception>', views.handler403, name='Error403'),
	path('404/<str:exception>', views.handler404, name='Error404'),
	path('500/', views.handler500, name='Error500'),
    path('benchmark/<int:pk>', views.benchmarkTesting, name="BenchmarkTesting")
]
