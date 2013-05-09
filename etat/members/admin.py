from django.contrib import admin

from suit.admin import SortableModelAdmin

import models


class AddressAdminInline(admin.StackedInline):
    model = models.Address
    extra = 0


class RoleAdminInline(admin.TabularInline):
    model = models.Role
    raw_id_fields = ('department',)
    extra = 0


class MemberAdmin(admin.ModelAdmin):
    inlines = [
        RoleAdminInline,
        AddressAdminInline,
    ]


class RoleTypeAdmin(SortableModelAdmin):
    sortable = 'order'

admin.site.register(models.Member, MemberAdmin)

admin.site.register(models.RoleType, RoleTypeAdmin)
