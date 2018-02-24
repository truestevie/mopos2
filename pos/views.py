from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import ShoppingBasket, ItemTemplate, Item, SubItemTemplate, SubItem


def show_basket(request):
    sb = ShoppingBasket.objects.filter(lifecycle="OPEN").first()
    if not sb:
        sb = ShoppingBasket.objects.create_shopping_basket()
    template_list = ItemTemplate.objects.filter(available=True)
    item_list = Item.objects.filter(shopping_basket=sb)
    print("---Item List----", item_list)
    kitchen_item_list = SubItem.objects.filter(shopping_basket=sb)
    #for sit in SubItemTemplate.objects.all():
    #    print("---", sit.description, sit.item_template)
    sub_item_template_dict = {}
    for item in item_list:
        sub_item_template_list = SubItemTemplate.objects.filter(item_template=item.item_template, available=True)
        if sub_item_template_list.count() > 1:
            print("Number of available sub items:", sub_item_template_list.count())
            print(item.id, sub_item_template_list)
            number_of_linked_sub_items = SubItem.objects.filter(item=item).count()
            if(number_of_linked_sub_items == 0):
                sub_item_template_dict[item] = sub_item_template_list
        # elif sub_item_template_list.count() = 1:

    print("---de dict van sub items---", sub_item_template_dict)
    return render(request, 'pos/basket.html', {'basket': sb,
                                               'template_list': template_list,
                                               'item_list': item_list,
                                               'kitchen_item_list': kitchen_item_list,
                                               'select_sub_items_dict': sub_item_template_dict
                                               })

def reset_table_number(request, shopping_basket_id):
    basket = ShoppingBasket.objects.get(pk=shopping_basket_id)
    basket.table_number = 1
    basket.save()
    return HttpResponseRedirect("/pos/basket")

def increment_table_number(request, shopping_basket_id, increment_value):
    basket = ShoppingBasket.objects.get(pk=shopping_basket_id)
    basket.table_number += increment_value
    basket.save()
    return HttpResponseRedirect("/pos/basket")

def close_basket(request, shopping_basket_id):
    basket = ShoppingBasket.objects.get(pk=shopping_basket_id)
    basket.lifecycle = 'CLOSED'
    basket.save()
    return HttpResponseRedirect("/pos/basket")

def add_item_to_basket(request, shopping_basket_id, item_template_id):
    new_basket_item = Item.objects.create_item(shopping_basket_id=shopping_basket_id, item_template_id=item_template_id)
    sub_item_template_list = SubItemTemplate.objects.filter(item_template__id = item_template_id, available = True)
    print("Number of available sub items for new basket item:", sub_item_template_list.count())
    if(sub_item_template_list.count() == 1):
        SubItem.objects.create_sub_item(shopping_basket_id=shopping_basket_id,
                                        item_id=new_basket_item.id,
                                        sub_item_template=sub_item_template_list.first())
    return HttpResponseRedirect("/pos/basket")


def remove_item_from_basket(request, shopping_basket_id, item_id):
    item = Item.objects.filter(id=item_id).first()
    sb = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
    sb.number_of_items -= 1
    sb.total_price -= item.unit_price
    sb.save()
    item.delete()
    return HttpResponseRedirect("/pos/basket")


def add_sub_item_to_item(request, shopping_basket_id, item_id, sub_item_template_id):
    SubItem.objects.create_sub_item(shopping_basket_id=shopping_basket_id,
                            item_id=item_id,
                            sub_item_template=SubItemTemplate.objects.filter(id=sub_item_template_id).first())
    return HttpResponseRedirect("/pos/basket")

