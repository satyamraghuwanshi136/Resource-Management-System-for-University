from django.contrib import admin
from .models import Iteminfo
from .models import Assignitem_info,Maintainitem,Replaceitem,Removeitem


admin.site.register(Iteminfo)
admin.site.register(Assignitem_info)
admin.site.register(Maintainitem)
admin.site.register(Replaceitem)
admin.site.register(Removeitem)
