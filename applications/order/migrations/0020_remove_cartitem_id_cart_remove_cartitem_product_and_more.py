# Generated by Django 4.1.7 on 2023-05-05 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_cartitem_id_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='id_cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
