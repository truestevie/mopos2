# Generated by Django 2.0.2 on 2018-02-23 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0011_auto_20180223_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='subitemtemplate',
            name='item_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos.ItemTemplate'),
        ),
    ]