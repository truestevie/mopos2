from django.urls import path
from .views import show_basket, reset_table_number, close_basket, increment_table_number, add_item_to_basket,\
    remove_item_from_basket, add_sub_item_to_item, show_transaction, receive_cash, remove_cash, receive_cents, \
    add_electronic_payment_with_automatic_value, show_kitchen_items, mark_as_printed, show_statistics, \
    export_items, export_sub_items, export_shopping_baskets, remove_x_items_from_basket, show_cash_overview
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', show_basket, name='show_basket'),
    path('basket/', show_basket, name='show_basket'),
    path('basket/<int:shopping_basket_id>/reset/', reset_table_number, name='reset_table_number'),
    path('basket/<int:shopping_basket_id>/increment_table_number/<int:increment_value>/',
         increment_table_number,
         name='increment_table_number'),
    path('basket/<int:shopping_basket_id>/receive_cash/<int:cash_received>/', receive_cash, name='receive_cash'),
    path('basket/<int:shopping_basket_id>/remove_cash/<int:cash_id>/', remove_cash, name='remove_cash'),
    path('basket/<int:shopping_basket_id>/receive_cents/<int:cents_received>/', receive_cents, name='receive_cents'),
    path('basket/<int:shopping_basket_id>/receive_electronic_payment/automatic/',
         add_electronic_payment_with_automatic_value,
         name='add_electronic_payment_with_automatic_value'),
    # path('basket/<int:shopping_basket_id>/receive_electronic_payment/<int:electronic_received>/<int:electronic_cents_received/',
    #     receive_electronic_payment, name='receive_electronic_payment'),
    path('basket/<int:shopping_basket_id>/close_basket/', close_basket, name='close_basket'),
    path('basket/<int:shopping_basket_id>/add_item/<int:item_template_id>/<int:number_of_items>/',
         add_item_to_basket,
         name='add_item_to_basket'),
    path('basket/<int:shopping_basket_id>/remove_item/<int:item_id>/',
         remove_item_from_basket,
         name='remove_item_from_basket'),
    path('basket/<int:shopping_basket_id>/remove_x_items/<int:item_id>/<int:number_of_items>/',
         remove_x_items_from_basket,
         name='remove_x_items_from_basket'),
    path('basket/<int:shopping_basket_id>/item/<int:item_id>/add_sub_item/<int:sub_item_template_id>/',
         add_sub_item_to_item,
         name='add_sub_item_to_item'),
    path('transaction/<int:shopping_basket_id>/', show_transaction, name='transaction'),
    path('basket/printer/', show_kitchen_items, name='show_kitchen_items'),
    path('basket/<int:shopping_basket_id>/printer/mark_as_printed/', mark_as_printed, name='mark_as_printed'),
    path('statistics/', show_statistics, name='show_statistics'),
    path('export/items/', export_items, name='export_items'),
    path('export/subitems/', export_sub_items, name='export_sub_items'),
    path('export/shoppingbaskets/', export_shopping_baskets, name='export_shopping_baskets'),
    path('overview/', show_cash_overview, name='show_cash_overview'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/pos/login'}, name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('logout/', logout, name='logout'),


]
