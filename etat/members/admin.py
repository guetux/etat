from django.contrib import admin

from suit.admin import SortableModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

import models


class AddressAdminInline(admin.StackedInline):
    model = models.Address
    extra = 0


class RoleAdminInline(admin.TabularInline):
    model = models.Role
    raw_id_fields = ('department', 'type')
    extra = 0


class MemberAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('scout_name', 'first_name', 'last_name')

    inlines = [
        RoleAdminInline,
        AddressAdminInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('scout_name', 'first_name', 'last_name', 'portrait',
                'gender', 'birthday', 'email', 'mobile')
        }),
        ('Notes', {
            'classes': ('collapse',),
            'fields': ('notes',),
        }),
    )


class RoleTypeAdmin(SortableModelAdmin):
    sortable = 'order'

admin.site.register(models.Member, MemberAdmin)

admin.site.register(models.RoleType, RoleTypeAdmin)
