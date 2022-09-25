from django import forms
from . models import Iteminfo

class PostForm(forms.ModelForm):
    class Meta(object):
        model = Iteminfo
        fields = ("item_id","item_name", "company", "purchase_date", "qty", "Pur_from", "order_ref", "order_date",
                  "in_no","spec", "warn", "ind_pri", "auth","tot_pri","photo")

    # def index(View):
    #     items =Item_info.objects.filter(item_id='item_id',status=0).count()
    #     print items

    # def clean_item_id(self):
    #     item_id = self.cleaned_data.get('item_id')
    #     for instance in Item_info.objects.all():
    #         if instance.item_id == item_id :
    #             raise forms.ValidationError('There is Item Id '+ item_id)
    #     return item_id

