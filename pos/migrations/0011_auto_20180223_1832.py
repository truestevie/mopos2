# Generated by Django 2.0.2 on 2018-02-23 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0010_auto_20180223_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubItemTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('description', models.CharField(max_length=30)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-id']},
        ),
    ]
