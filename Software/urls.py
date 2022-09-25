from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('manage/', views.manage, name='Manage'),

    path('add/',views.add, name='Add'),
    path('add_man/',views.add_man, name='Add_man'),
    path('add_mant/<maint_id>', views.add_mant, name='Add_mant'),

    path('total/',views.total,name='Total'),
    path('view_man/', views.view_man, name="View_man"),

    path('report_info/', views.report_info, name='Report_Info'),
    path('report_manage/', views.report_manage, name='Report_Manage'),
    path('report_valid/', views.report_valid, name='Report_valid'),
    path('report_expire/', views.report_expire, name='Report_expire'),

    path('update/<prod_id>',views.update,name='Update'),
    path('update_man/<main_id>',views.update_man,name ="Update_man"),

    path('delete/', views.delete, name='Delete'),
    path('delete_man',views.delete_man, name='Delete_man'),

    path('del_event/<prod_id>', views.del_event, name='Del_event'),
    path('del_man/<main_id>',views.del_man,name="Del_man"),

    path('valid',views.valid,name="Valid"),
    path('expire',views.expire,name="Expire"),
]
