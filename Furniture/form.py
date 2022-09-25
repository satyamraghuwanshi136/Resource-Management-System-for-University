from django import forms
from . models import Assignitem_info,Maintainitem,Replaceitem,Removeitem


class AssignForm(forms.ModelForm):
    class Meta(object):
        model = Assignitem_info
        fields = ("item_id","quantity","lab_name","assign_date","assigned_by")

class MainForm(forms.ModelForm):
    class Meta(object):
        model = Maintainitem
        fields = ("item_id","add_date", "qty" ,"added_by","given")

class ReplaceForm(forms.ModelForm):
    class Meta(object):
        model =Replaceitem
        fields = ("item_id", "qty", "date", "added_by")

class RemoveForm(forms.ModelForm):
    class Meta(object):
        model =Removeitem
        fields = ("item_id", "qty", "date", "added_by")