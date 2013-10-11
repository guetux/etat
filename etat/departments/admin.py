from django.contrib import admin
from django.utils.safestring import mark_safe

from suit.admin import SortableModelAdmin

from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Department, DepartmentType


class DepartmentTypeAdmin(SortableModelAdmin):
    pass


class DepartmentAdmin(DjangoMpttAdmin):
    list_display = ('name_indented',)
    search_fields = ('name',)
    list_filter = ('type',)
    sortable = 'order'

    def name_indented(self, obj):
        indent = 10 * obj.level
        output = u'<span style="padding-left: %spx">%s</span>' % (indent, obj)
        return mark_safe(output)

admin.site.register(DepartmentType, DepartmentTypeAdmin)
admin.site.register(Department, DepartmentAdmin)
