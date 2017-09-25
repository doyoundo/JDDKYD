from django.contrib import admin
from models import InstructorKey, Section

# Register your models here.
class InstructorKeyAdmin(admin.ModelAdmin):
	list_display = ['key',]

# Register your models here.
class SectionAdmin(admin.ModelAdmin):
	list_display = ['name',]

admin.site.register(InstructorKey, InstructorKeyAdmin)
admin.site.register(Section, SectionAdmin)