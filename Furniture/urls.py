from django.http import response
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from .models import *

from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('additem/',views.additem, name='additem'),
    path('totalstock/',views.totalstock,name='totalstock'),
    path('specifications/<spe_id>',views.specifications,name='specifications'),
    path('order_detail/<ord_id>',views.order_detail,name='order_detail'),
    path('purchase_detail/<pur_id>',views.purchase_detail,name='purchase_detail'),

    path('update/<prod_id>',views.update,name='update'),

    path('assignitem/',views.assignItem, name='assignitem'),
    path('itemassign/<ass_id>',views.itemassign, name='itemassign'),
    path('viewassign/',views.viewAssign, name="viewassign"),

    path('assign_ret/<return_id>',views.assign_ret, name="assign_ret"),
    path('add_return',views.add_return, name="add_return"),

    path('addmain/',views.addmain,name='addmain'),
    path('add_main/<man_id>',views.add_main,name='add_main'),
    path('viewmain/',views.viewmain,name="viewmain"),

    path('main_ret/<ret_id>',views.main_ret, name="main_ret"),
    path('return_main',views.return_main, name="return_main"),

    path('main_replace/<rep_id>', views.main_replace, name="main_replace"),
    path('replace_main', views.replace_main, name="replace_main"),

    path('replace_ret/<ret_id>', views.replace_ret, name="replace_ret"),
    path('replace_items', views.replace_items, name="replace_items"),
    path('return_replace',views.return_replace, name="return_replace"),

    path('main_remove/<rem_id>', views.main_remove, name="main_remove"),
    path('remove_main', views.remove_main, name="remove_main"),
    path('remove_items', views.remove_items, name="remove_items"),

    path('report_totalstock', views.report_totalstock, name="report_totalstock"),
    path('report_assign', views.report_assign, name="report_assign"),
    path('report_maintenance', views.report_maintenance, name="report_maintenance"),
    path('report_replace', views.report_replace, name="report_replace"),
    path('report_remove', views.report_remove, name="report_remove"),

]