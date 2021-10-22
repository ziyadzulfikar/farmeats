# Generated by Django 3.2.7 on 2021-10-17 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0006_delete_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.BigIntegerField()),
                ('address', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=50)),
                ('zip', models.IntegerField()),
                ('paymentMethod', models.CharField(max_length=20)),
                ('products', models.CharField(default=0, max_length=100)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('delivery', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]