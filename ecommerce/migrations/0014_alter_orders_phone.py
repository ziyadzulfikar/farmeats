# Generated by Django 3.2.7 on 2021-10-22 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_expenses_totalexpense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.BigIntegerField(default=0),
        ),
    ]
