from django.contrib import admin
from .models import *
import base64
from django.utils.html import format_html
# Register your models here.


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
    
    '''
    list_display = ('user_photo', 'First', 'Last', 'Email', 'Enrollment', 'custom_contact', 'Department_id', 'Course_id', 'Branch_id', 'Semester_id',)
    ordering = ('First',)
    search_fields = ('First', 'Last', 'Email', 'Enrollment', 'Contact',)
    fieldsets = (('Required Information', {'description': "These fields are required.", 'fields': ('First', 'Last', 'Email', 'Enrollment', 'Contact', 'Department_id', 'Course_id', 'Branch_id', 'Semester_id',)}), ('Default Information', {'classes': ('collapse',), 'fields': ('Photo',)}),)
    readonly_fields = ('Photo',)

    def custom_contact(self, obj):
        return format_html('<a href="tel:' + str(obj.Contact) + '">' + str(obj.Contact) + '</a>')

    custom_contact.short_description = 'Contact'
    custom_contact.allow_tags = True

    def user_photo(self, obj):
        return format_html('<img style="width: 96px; height 96px;" src="data:;base64,{}">', obj.Photo)

    user_photo.short_description = 'Photo'
    user_photo.allow_tags = True
    '''

@admin.register(Attendence)
class AttendenceAdmin(admin.ModelAdmin):
    pass


@admin.register(SendGridAPIKey)
class SendGridAPIKeyAdmin(admin.ModelAdmin):
    pass

@admin.register(TwilioAPIKey)
class SendGridAPIKeyAdmin(admin.ModelAdmin):
    pass

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    pass

@admin.register(FacultyAssigned)
class FacultyAssignedAdmin(admin.ModelAdmin):
    pass