# Generated by Django 4.2.2 on 2023-07-09 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Subtotal')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Descuento por puntos')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Total')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Cantidad')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Subtotal')),
                ('id_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart', verbose_name='ID del pedido')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Producto')),
            ],
        ),
    ]
