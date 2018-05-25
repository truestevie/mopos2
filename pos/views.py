from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import ShoppingBasket, ItemTemplate, Item, SubItemTemplate, SubItem, Cash, CashRegister
from .resources import ItemResource, SubItemResource, ShoppingBasketResource

# from escpos.connections import getNetworkPrinter


@login_required
def show_transaction(request, shopping_basket_id):
    sb = ShoppingBasket.objects.get(pk=shopping_basket_id)
    cash_received_list = Cash.objects.filter(shopping_basket=sb, electronic=False)
    electronic_received_list = Cash.objects.filter(shopping_basket=sb, electronic=True)
    cash_to_return = sb.cash_received_physical + sb.cash_received_electronic - sb.total_price
    cash_to_receive = sb.total_price - sb.cash_received_physical - sb.cash_received_electronic
    if cash_to_return < 0:
        cash_color = "red"
    else:
        cash_color = "green"
    return render(request, 'pos/transaction.html',
                  {'basket': sb,
                   'cash_received_list': cash_received_list,
                   'electronic_received_list': electronic_received_list,
                   'cash_to_return': cash_to_return,
                   'cash_color': cash_color,
                   'cash_to_receive': cash_to_receive,
                   })


@login_required(login_url='/pos/login')
def show_basket(request):
    print("---Showing the basket for user {}---".format(request.user))
    sb = ShoppingBasket.objects.filter(lifecycle="OPEN", user=request.user).first()
    if not sb:
        sb = ShoppingBasket.objects.create_shopping_basket(request.user)
    template_list = ItemTemplate.objects.filter(available=True).order_by('print_order')
    item_list = Item.objects.filter(shopping_basket=sb).order_by('item_template__print_order')
    print("---Item List----", item_list)
    kitchen_item_list = SubItem.objects.filter(shopping_basket=sb)
    # for sit in SubItemTemplate.objects.all():
    #    print("---", sit.description, sit.item_template)
    sub_item_template_dict = {}
    for item in item_list:
        sub_item_template_list = SubItemTemplate.objects.filter(item_template=item.item_template, available=True)
        if sub_item_template_list.count() > 1:
            print("Number of available sub items:", sub_item_template_list.count())
            print(item.id, sub_item_template_list)
            number_of_linked_sub_items = SubItem.objects.filter(item=item).count()
            if number_of_linked_sub_items == 0:
                sub_item_template_dict[item] = sub_item_template_list
        # elif sub_item_template_list.count() = 1:
    cash_received_list = Cash.objects.filter(shopping_basket=sb)
    cash_to_return = sb.cash_received_physical + sb.cash_received_electronic - sb.total_price
    cash_color = ""
    if cash_to_return < 0:
        cash_color = "red"

    print("---de dict van sub items---", sub_item_template_dict)
    print("---de cash received list---", cash_received_list)
    print("---cash to return---", cash_to_return)
    return render(request, 'pos/basket.html', {'basket': sb,
                                               'template_list': template_list,
                                               'item_list': item_list,
                                               'kitchen_item_list': kitchen_item_list,
                                               'select_sub_items_dict': sub_item_template_dict,
                                               'cash_received_list': cash_received_list,
                                               'cash_to_return': cash_to_return,
                                               'cash_color': cash_color,
                                               })


def show_cash_overview(request):
    print("---Showing the overview for user {}---".format(request.user))
    cash_register, created = CashRegister.objects.get_or_create(name='BigVault')
    cash_start = cash_register.initial_physical
    cash_current = cash_register.initial_physical + cash_register.sales_physical
    revenue_electronic = cash_register.sales_electronic
    revenue_cash = cash_register.sales_physical
    revenue_total = cash_register.sales_physical + cash_register.sales_electronic
    template_list = ItemTemplate.objects.filter(number_sold__gt=0).order_by('print_order')
    return render(request, 'pos/cash_overview.html', {'cash_start': cash_start,
                                                      'cash_current': cash_current,
                                                      'revenue_electronic': revenue_electronic,
                                                      'revenue_cash': revenue_cash,
                                                      'revenue_total': revenue_total,
                                                      'template_list': template_list,
                                                      })


@login_required
def receive_cash(request, shopping_basket_id, cash_received):
    Cash.objects.add_cash_item(shopping_basket_id, cash_received)
    return HttpResponseRedirect("/pos/transaction/{}/".format(shopping_basket_id))


@login_required
def receive_cents(request, shopping_basket_id, cents_received):
    Cash.objects.add_cash_cents_item(shopping_basket_id, cents_received)
    return HttpResponseRedirect("/pos/transaction/{}/".format(shopping_basket_id))


@login_required
def remove_cash(request, shopping_basket_id, cash_id):
    Cash.objects.remove_cash_item(shopping_basket_id, cash_id)
    return HttpResponseRedirect("/pos/transaction/{}/".format(shopping_basket_id))


@login_required
def add_electronic_payment_with_automatic_value(request, shopping_basket_id):
    Cash.objects.add_electronic_payment_with_automatic_value(shopping_basket_id)
    return HttpResponseRedirect("/pos/transaction/{}/".format(shopping_basket_id))


@login_required
def reset_table_number(request, shopping_basket_id):
    basket = ShoppingBasket.objects.get(pk=shopping_basket_id)
    basket.table_number = 1
    basket.save()
    return HttpResponseRedirect("/pos/basket")


@login_required
def increment_table_number(request, shopping_basket_id, increment_value):
    basket = ShoppingBasket.objects.get(pk=shopping_basket_id)
    basket.table_number += increment_value
    basket.save()
    return HttpResponseRedirect("/pos/basket")


@login_required
def close_basket(request, shopping_basket_id):
    print("---Closing basket---")
    basket = ShoppingBasket.objects.get(pk=shopping_basket_id)
    basket.lifecycle = 'CLOSED'
    basket.save()
    cash_register, created = CashRegister.objects.get_or_create(name='BigVault')
    cash_register.sales_physical += basket.total_price - basket.cash_received_electronic
    cash_register.sales_electronic += basket.cash_received_electronic
    cash_register.save()

    item_list = Item.objects.filter(shopping_basket=basket).order_by('print_order')
    print("---Item List---", item_list)
    for item in item_list:
        item_template = ItemTemplate.objects.get(code=item.code)
        item_template.number_sold += item.number_of_items
        item_template.save()
        print(item_template.description, item_template.number_sold)


    # https://pypi.python.org/pypi/python-printer-escpos/0.0.3

    # printer = getNetworkPrinter()(host='10.1.1.207')
    # printer.text("Hello World")
    # printer.lf()
    # printer.cutPaper()

    # https://python-escpos.readthedocs.io/en/latest/user/methods.html

    return HttpResponseRedirect("/pos/basket")


@login_required
def add_item_to_basket(request, shopping_basket_id, item_template_id, number_of_items):
    new_basket_item = Item.objects.create_item(shopping_basket_id=shopping_basket_id,
                                               item_template_id=item_template_id,
                                               number_of_items=number_of_items)
    sub_item_template_list = SubItemTemplate.objects.filter(item_template__id=item_template_id, available=True)
    print("Number of available sub items for new basket item:", sub_item_template_list.count())
    if sub_item_template_list.count() == 1:
        SubItem.objects.create_sub_item(shopping_basket_id=shopping_basket_id,
                                        item_id=new_basket_item.id,
                                        sub_item_template=sub_item_template_list.first())
    return HttpResponseRedirect("/pos/basket")


@login_required
def remove_item_from_basket(request, shopping_basket_id, item_id):
    item = Item.objects.filter(id=item_id).first()
    sb = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
    sb.number_of_items -= item.number_of_items
    sb.total_price -= item.unit_price * item.number_of_items
    sb.save()
    item.delete()
    return HttpResponseRedirect("/pos/basket")


@login_required
def remove_x_items_from_basket(request, shopping_basket_id, item_id, number_of_items):
    item = Item.objects.filter(id=item_id).first()
    sb = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
    if item.number_of_items > number_of_items:
        item.number_of_items -= number_of_items
        item.total_price -= number_of_items * item.unit_price
        item.save()
        sb.number_of_items -= number_of_items
        sb.total_price -=  number_of_items * item.unit_price
        sb.save()
    elif item.number_of_items == number_of_items:
        item.delete()
        sb.number_of_items -= number_of_items
        sb.total_price -= number_of_items * item.unit_price
        sb.save()
    else:
        print("---Can not remove that amount of items from the basket---")
    return HttpResponseRedirect("/pos/basket")


@login_required
def add_sub_item_to_item(request, shopping_basket_id, item_id, sub_item_template_id):
    SubItem.objects.create_sub_item(shopping_basket_id=shopping_basket_id,
                                    item_id=item_id,
                                    sub_item_template=SubItemTemplate.objects.filter(id=sub_item_template_id).first())
    return HttpResponseRedirect("/pos/basket")


@login_required
def show_kitchen_items(request):
    oldest_unprinted_order = ShoppingBasket.objects.filter(printed=False).first()
    print("+++oldestUnprintedOrder+++", oldest_unprinted_order)
    if oldest_unprinted_order:
        unprinted_kitchen_item_list = SubItem.objects.filter(shopping_basket__id=oldest_unprinted_order.id)
        print("+++unprintedKitchenItems", unprinted_kitchen_item_list)
    else:
        unprinted_kitchen_item_list = ()
    return render(request, 'pos/kitchen_printer.html',
                  {'unprinted_order': oldest_unprinted_order,
                   'unprinted_kitchen_items': unprinted_kitchen_item_list,
                   })


@login_required
def mark_as_printed(request, shopping_basket_id):
    sb = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
    sb.printed = True
    sb.save()
    return HttpResponseRedirect("/pos/basket/printer")


@login_required
def show_statistics(request):
    cash_register, created = CashRegister.objects.get_or_create(name='BigVault')
    revenue = cash_register.sales_physical + cash_register.sales_electronic
    current_cash = cash_register.initial_physical + cash_register.sales_physical
    return render(request, 'pos/statistics.html',
                  {'revenue': revenue,
                   'current_cash': current_cash
                   })


def export_items(request):
    # Run an export of the collected data
    # https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
    item_resource = ItemResource()
    dataset = item_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items.csv"'
    return response


def export_sub_items(request):
    # Run an export of the collected data
    # https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
    sub_item_resource = SubItemResource()
    dataset = sub_item_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subitems.csv"'
    return response


def export_shopping_baskets(request):
    # Run an export of the collected data
    # https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
    shopping_basket_resource = ShoppingBasketResource()
    dataset = shopping_basket_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shoppingbaskets.csv"'
    return response

def logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
