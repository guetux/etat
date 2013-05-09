from django.contrib import admin

from suit.admin import SortableModelAdmin

from mptt.admin import MPTTModelAdmin

from .models import Department, DepartmentType


class DepartmentTypeAdmin(SortableModelAdmin):
    pass


class DepartmentAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    list_display = ('name',)
    list_filter = ('type',)
    sortable = 'order'

admin.site.register(DepartmentType, DepartmentTypeAdmin)
admin.site.register(Department, DepartmentAdmin)
