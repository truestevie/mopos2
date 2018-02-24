from django.contrib import admin
from .models import ShoppingBasket, Item, ItemTemplate, SubItemTemplate, SubItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'unit_price', 'print_order', 'available', 'shopping_basket')
    ordering = ('print_order',)

class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'unit_price', 'print_order', 'available')
    ordering = ('print_order',)

class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_of_items', 'total_price', 'lifecycle', 'table_number')
    ordering = ('-id',)

class SubItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'available')
    ordering = ('code',)
    filter_horizontal = ('item_template',)


admin.site.register(ShoppingBasket, ShoppingBasketAdmin)
admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SubItemTemplate, SubItemTemplateAdmin)
admin.site.register(SubItem)
