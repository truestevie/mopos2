# Generated by Django 2.0.2 on 2018-02-23 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_item_itemtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplate',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
