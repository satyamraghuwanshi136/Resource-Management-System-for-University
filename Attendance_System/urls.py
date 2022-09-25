from django.contrib import admin
from django.urls import path, include
from Authentication import views as aview
from django.conf.urls import url
from Resources import views as ErrorView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', aview.loginAuth),
    path('admin/', admin.site.urls),
    path('api/v1/', include(('Resources.urls', 'Resources'), namespace='ResourcesAPI')),
    path('manual-auth/', include(('Authentication.urls', 'Authentication'), namespace='Authentication')),
    path('manage/', include(('Administration.urls', 'Administration'), namespace='Administration')),
    path('mails/', include(('Mails.urls', 'Mails'), namespace='Mails')),
    path('students/', include(('Students.urls', 'Students'), namespace='Students')),
    path('resources/', include(('Resources.urls', 'Resources'), namespace='Resources')),
    path('department/', include(('Department.urls', 'Department'), namespace='Department')),
    path('faculty/', include(('Faculty.urls', 'Faculty'), namespace='Faculty')),
    path('attendance/', include(('Attendance.urls', 'Attendance'), namespace='Attendance')),
    path('marks/', include(('Marks.urls', 'Marks'), namespace='Marks')),
    path('software/', include(('Software.urls', 'Software'), namespace='Software')),
    path('hardware/', include(('hardware.urls', 'hardware'), namespace='hardware')),
    path('furniture/', include(('Furniture.urls', 'Furniture'), namespace='Furniture')),
    path('library/', include(('Library.urls', 'Library'), namespace='Library')),
    path('thesis/', include(('Thesis.urls', 'Thesis'), namespace='Thesis')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]

handler400 = ErrorView.handler400
handler403 = ErrorView.handler403
handler404 = ErrorView.handler404
handler500 = ErrorView.handler500

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()