from django.contrib import admin
from .models import Item, ItemTemplate, SubItemTemplate, SubItem, Cash, ShoppingBasket, CashRegister


class ItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'unit_price', 'print_order', 'available', 'shopping_basket', 'item_template')
    ordering = ('print_order',)


class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'unit_price', 'print_order', 'available', 'number_sold')
    ordering = ('print_order',)


class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'number_of_items', 'total_price', 'lifecycle', 'table_number', 'last_change_date')
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
admin.site.register(Cash)
admin.site.register(CashRegister)
