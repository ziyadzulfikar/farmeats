# Generated by Django 3.2.7 on 2021-10-17 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0003_auto_20211017_1134'),
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
                ('delivery', models.CharField(max_length=50)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]