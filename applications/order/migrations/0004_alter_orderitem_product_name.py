# Generated by Django 4.2.3 on 2023-07-20 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_orderitem_product_orderitem_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product_name',
            field=models.CharField(max_length=100, verbose_name='Producto'),
        ),
    ]