from django.contrib import admin
from .models import Item_info
from .models import Assign_item_info,Maintain_item,Replace_item,Remove_item


admin.site.register(Item_info)
admin.site.register(Assign_item_info)
admin.site.register(Maintain_item)
admin.site.register(Replace_item)
admin.site.register(Remove_item)
