# Generated by Django 2.0.2 on 2018-02-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0009_item_shopping_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingbasket',
            name='lifecycle',
            field=models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], default='OPEN', max_length=10),
        ),
        migrations.AlterField(
            model_name='shoppingbasket',
            name='table_number',
            field=models.IntegerField(default=1),
        ),
    ]
