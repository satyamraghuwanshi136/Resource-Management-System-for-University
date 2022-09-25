from django.contrib import admin
from .models import Thesis

# Register your models here.
@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    pass
