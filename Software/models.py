from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.base import Model


# Create your models here.
class Software_info(models.Model) :
    Soft_id = models.IntegerField(primary_key=True)
    SName = models.CharField(max_length=50)
    Users = models.PositiveIntegerField(default=1)
    Tot_users=models.PositiveIntegerField(default=1)
    PurD = models.DateField()
    ExpD = models.DateField()
    # Keys = models.IntegerField()
    PurForSub = models.CharField(max_length=50)
    ind_pri = models.PositiveIntegerField()
    # date = models.DateField()
    auth = models.CharField(max_length=50)

    def __str__(self):
        return str(self.Soft_id)


class Software_manage(models.Model) :
    Soft_id = models.ForeignKey(Software_info, on_delete=models.DO_NOTHING)
    LabI = models.CharField(max_length=20)
    Users = models.PositiveIntegerField()
    assigned_by = models.CharField(max_length=50)
    assign_date = models.DateField()

    def __str__(self):
        return str(self.Soft_id)