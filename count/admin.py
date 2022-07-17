from django.contrib import admin

from count.models import Party, Member, Purchase, PurchaseExclude


admin.site.register(Party)
admin.site.register(Member)
admin.site.register(Purchase)
admin.site.register(PurchaseExclude)
