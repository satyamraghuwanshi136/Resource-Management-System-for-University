from django.db import models
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from Resources.models import *

# Create your models here.
class Iteminfo(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=50)
    purchase_date = models.DateField()
    qty = models.PositiveIntegerField(default=1)
    tot_qty = models.PositiveIntegerField(default=1)
    Pur_from = models.CharField(max_length=50)
    order_ref = models.CharField(max_length=50)
    order_date = models.DateField()
    in_no = models.PositiveIntegerField()
    spec = models.CharField(max_length=50)
    warn = models.DateField()
    ind_pri = models.PositiveIntegerField()
    tot_pri = models.PositiveIntegerField()
    photo = models.ImageField(upload_to="img/%y")
    auth = models.CharField(max_length=50)


    def __str__(self):
        return str(self.item_id)

class Assignitem_info(models.Model):
    item_id = models.ForeignKey(Iteminfo, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)
    lab_name = models.CharField(max_length=50,null="True")
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING,null="True")
    assigned_by = models.CharField(max_length=50)
    assign_date = models.DateField()

    def __str__(self):
        return str(self.item_id)


class Maintainitem(models.Model):
    item_id = models.ForeignKey(Iteminfo, on_delete=models.DO_NOTHING)
    qty = models.PositiveIntegerField(default=1)
    given=models.CharField(max_length=50)
    add_date = models.DateField()
    added_by = models.CharField(max_length=50)

    def __str__(self):
        return str(self.item_id)

class Replaceitem(models.Model):
    item_id = models.ForeignKey(Iteminfo, on_delete=models.DO_NOTHING)
    qty = models.PositiveIntegerField(default=1)
    date = models.DateField()
    added_by = models.CharField(max_length=50)

    def __str__(self):
        return str(self.item_id)


class Removeitem(models.Model):
    item_id = models.ForeignKey(Iteminfo, on_delete=models.DO_NOTHING)
    qty = models.PositiveIntegerField(default=1)
    date = models.DateField()
    added_by = models.CharField(max_length=50)

    def __str__(self):
        return str(self.item_id)