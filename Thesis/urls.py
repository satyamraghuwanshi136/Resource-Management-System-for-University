from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('AddThesis/', views.AddThesis, name='AddThesis'),
    # path('Message/',views.Message,name='Message'),
    path('Search/',views.Search,name='Search'),
    path('List/',views.ListThesis,name='List'),
    path('Remove/',views.Remove,name='Remove'),
    path('RemoveThesis/<tname>/',views.RemoveThesis,name='RemoveThesis'),

    
]
