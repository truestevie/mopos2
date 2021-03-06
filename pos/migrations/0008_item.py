# Generated by Django 2.0.2 on 2018-02-23 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0007_auto_20180223_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=30)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('print_order', models.SmallIntegerField(default=0)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['print_order'],
            },
        ),
    ]
