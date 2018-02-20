# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-20 16:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date')),
                ('modified', models.DateTimeField(editable=False, verbose_name='Modified date')),
                ('is_active', models.BooleanField(default=False, verbose_name='Activo')),
                ('is_visibility', models.BooleanField(default=False, verbose_name='Visible')),
                ('price', models.DecimalField(decimal_places=3, default=False, max_digits=10, verbose_name='Precio')),
                ('price_offer', models.DecimalField(decimal_places=3, default=False, max_digits=10, verbose_name='Precio de  Oferta')),
                ('offer_day_from', models.DateTimeField(verbose_name='Fecha de inicio de oferta')),
                ('offer_day_to', models.DateTimeField(verbose_name='Fecha de fin de oferta')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Product quantity')),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Product')),
            ],
        ),
    ]
