from django import forms
from . models import Software_info
from .models import Software_manage

class PostForm(forms.ModelForm):
    class Meta(object):
        model = Software_info
        fields = ("Soft_id","SName","Users","PurD","ExpD","PurForSub","ind_pri","auth")

class ManForm(forms.ModelForm):
    class Meta(object):
        model=Software_manage
        fields=("Soft_id","LabI","assigned_by","assign_date","Users")

