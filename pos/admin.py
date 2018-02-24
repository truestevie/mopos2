from django.contrib import admin
from .models import Item, ItemTemplate, SubItemTemplate, SubItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'unit_price', 'print_order', 'available', 'shopping_basket')
    ordering = ('print_order',)

class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'unit_price', 'print_order', 'available')
    ordering = ('print_order',)

class SubItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'available')
    ordering = ('code',)
    filter_horizontal = ('item_template',)


admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SubItemTemplate, SubItemTemplateAdmin)
admin.site.register(SubItem)
