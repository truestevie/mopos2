from import_export import resources
from .models import Item, SubItem, ShoppingBasket

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item

class SubItemResource(resources.ModelResource):
    class Meta:
        model = SubItem

class ShoppingBasketResource(resources.ModelResource):
    class Meta:
        model = ShoppingBasket