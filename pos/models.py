from django.db import models
import decimal

D = decimal.Decimal


class ShoppingBasketManager(models.Manager):
    def create_shopping_basket(self):
        if ShoppingBasket.objects.last():
            next_table_number = ShoppingBasket.objects.last().table_number + 1
        else:
            next_table_number = 1
        shopping_basket = self.create(table_number=next_table_number)
        return shopping_basket


class ShoppingBasket(models.Model):
    number_of_items = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_received_physical = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_received_electronic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)
    owner = models.SmallIntegerField(default=0)
    LIFECYCLE_CHOICES = (("OPEN", "Open"), ("CLOSED", "Closed"))
    lifecycle = models.CharField(max_length=10, choices=LIFECYCLE_CHOICES, default="OPEN")
    table_number = models.IntegerField(default=1)
    objects = ShoppingBasketManager()

    def receive_cash(self, cash_received):
        self.cash_received_physical += cash_received


class ItemTemplate(models.Model):
    code = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    print_order = models.SmallIntegerField(default=0)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['print_order']

    def __str__(self):
        return "{} ({})".format(self.description, self.code)


class ItemManager(models.Manager):
    def create_item(self, shopping_basket_id, item_template_id):
        shopping_basket = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
        item_template = ItemTemplate.objects.filter(pk=item_template_id).first()
        item = self.create(code=item_template.code,
                           description=item_template.description,
                           unit_price=item_template.unit_price,
                           shopping_basket=shopping_basket,
                           item_template=item_template)
        shopping_basket.total_price += item.unit_price
        shopping_basket.number_of_items += 1
        shopping_basket.save()
        return item


class Item(models.Model):
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    print_order = models.SmallIntegerField(default=0)
    available = models.BooleanField(default=True)
    shopping_basket = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)
    item_template = models.ForeignKey(ItemTemplate, on_delete=models.DO_NOTHING, null=True)
    objects = ItemManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{} ({})".format(self.description, self.code)


class SubItemTemplate(models.Model):
    code = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=30)
    available = models.BooleanField(default=True)
    item_template = models.ManyToManyField(ItemTemplate)

    def __str__(self):
        return "{} ({})".format(self.description, self.code)


class SubItemManager(models.Manager):
    def create_sub_item(self, shopping_basket_id, item_id, sub_item_template):
        shopping_basket = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
        print("sb:", shopping_basket)
        item = Item.objects.filter(pk=item_id).first()
        print("i", item)
        sub_item = self.create(code=sub_item_template.code,
                               description=sub_item_template.description,
                               shopping_basket=shopping_basket,
                               item=item)
        shopping_basket.save()
        return sub_item


class SubItem(models.Model):
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=30)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    shopping_basket = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE, null=True)
    objects = SubItemManager()

    class Meta:
        ordering = ['description', 'item__code']


class CashRegister(models.Model):
    initial_physical = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales_physical = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales_electronic = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transaction(models.Model):
    order = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)


class CashManager(models.Manager):
    def add_cash_item(self, shopping_basket_id, value):
        shopping_basket = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
        cash_item = self.create(shopping_basket=shopping_basket, value=value)
        shopping_basket.cash_received_physical += value
        shopping_basket.save()
        return cash_item

    def remove_cash_item(self, shopping_basket_id, cash_id):
        shopping_basket = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
        cash_item = Cash.objects.filter(pk=cash_id).first()
        if not cash_item.electronic:
            shopping_basket.cash_received_physical -= cash_item.value
        else:
            shopping_basket.cash_received_electronic -= cash_item.value
        shopping_basket.save()
        cash_item.delete()

    def add_cash_cents_item(self, shopping_basket_id, value):
        shopping_basket = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
        cash_item = self.create(shopping_basket=shopping_basket, value=value/100)
        shopping_basket.cash_received_physical += D(value/100)
        shopping_basket.save()
        return cash_item

    def add_electronic_payment_with_automatic_value(self, shopping_basket_id):
        shopping_basket = ShoppingBasket.objects.filter(pk=shopping_basket_id).first()
        electronic_value = shopping_basket.total_price - shopping_basket.cash_received_physical -\
                           shopping_basket.cash_received_electronic
        cash_item = self.create(shopping_basket=shopping_basket, value=electronic_value, electronic=True)
        shopping_basket.cash_received_electronic += electronic_value
        shopping_basket.save()
        return cash_item


class Cash(models.Model):
    shopping_basket = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    objects = CashManager()
    electronic = models.BooleanField(default=False)

    class Meta:
        ordering = ['-value']

    def __str__(self):
        return "{} ({})".format(self.value, self.shopping_basket)
