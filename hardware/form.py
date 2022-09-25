from django import forms
from . models import Assign_item_info,Maintain_item,Replace_item,Remove_item


class AssignForm(forms.ModelForm):
    class Meta(object):
        model = Assign_item_info
        fields = ("item_id","quantity","lab_name","assign_date","assigned_by")

class MainForm(forms.ModelForm):
    class Meta(object):
        model = Maintain_item
        fields = ("item_id","add_date", "qty" ,"added_by","given")

class ReplaceForm(forms.ModelForm):
    class Meta(object):
        model =Replace_item
        fields = ("item_id", "qty", "date", "added_by")

class RemoveForm(forms.ModelForm):
    class Meta(object):
        model =Remove_item
        fields = ("item_id", "qty", "date", "added_by")