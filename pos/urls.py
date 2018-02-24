from django.urls import path
from .views import show_basket, reset_table_number, close_basket, increment_table_number, add_item_to_basket,\
    remove_item_from_basket, add_sub_item_to_item, show_transaction, receive_cash, remove_cash, receive_cents

urlpatterns = [
    path('', show_basket, name='show_basket'),
    path('basket/', show_basket, name='show_basket'),
    path('basket/<int:shopping_basket_id>/reset/', reset_table_number, name='reset_table_number'),
    path('basket/<int:shopping_basket_id>/increment_table_number/<int:increment_value>/', increment_table_number, name='increment_table_number'),
    path('basket/<int:shopping_basket_id>/receive_cash/<int:cash_received>/', receive_cash, name='receive_cash'),
    path('basket/<int:shopping_basket_id>/remove_cash/<int:cash_id>/', remove_cash, name='remove_cash'),
    path('basket/<int:shopping_basket_id>/receive_cents/<int:cents_received>/', receive_cents, name='receive_cents'),
    path('basket/<int:shopping_basket_id>/close_basket/', close_basket, name='close_basket'),
    path('basket/<int:shopping_basket_id>/add_item/<int:item_template_id>/', add_item_to_basket, name='add_item_to_basket'),
    path('basket/<int:shopping_basket_id>/remove_item/<int:item_id>/', remove_item_from_basket, name='remove_item_from_basket'),
    path('basket/<int:shopping_basket_id>/item/<int:item_id>/add_sub_item/<int:sub_item_template_id>/', add_sub_item_to_item, name='add_sub_item_to_item' ),
    path('transaction/<int:shopping_basket_id>/', show_transaction, name='transaction'),
]
