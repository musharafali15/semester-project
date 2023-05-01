# Generated by Django 3.0.4 on 2020-04-13 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0072_product_minbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='auction_status',
            field=models.CharField(choices=[('S', 'Seller'), ('B', 'Buyer')], default='NF', max_length=2),
        ),
    ]
