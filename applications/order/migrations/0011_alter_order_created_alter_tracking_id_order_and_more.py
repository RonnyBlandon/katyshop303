# Generated by Django 4.1.7 on 2023-04-10 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_orderitem_unit_price_alter_shippingcompany_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='id_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_tracking', to='order.order', verbose_name='ID Orden'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='shipping_date',
            field=models.DateField(verbose_name='Fecha de envio'),
        ),
    ]
