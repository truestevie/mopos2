# Generated by Django 2.0.2 on 2018-02-23 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_itemtemplate_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtemplate',
            name='code',
            field=models.CharField(max_length=3, unique=True),
        ),
    ]
