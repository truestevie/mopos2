# Generated by Django 2.0.2 on 2018-02-23 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0006_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='itemtemplate_ptr',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
