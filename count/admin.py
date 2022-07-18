from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from count.models import Party, Member, Purchase, PurchaseExclude, PartyUser


class UserAdminConfig(UserAdmin):
    model = PartyUser
    search_fields = ('email', 'first_name', 'last_name',)
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('first_name',)
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'payment_method',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'payment_method')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


admin.site.register(PartyUser, UserAdminConfig)
admin.site.register(Party)
admin.site.register(Member)
admin.site.register(Purchase)
admin.site.register(PurchaseExclude)
