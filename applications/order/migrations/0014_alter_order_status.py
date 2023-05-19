# Generated by Django 4.1.7 on 2023-04-12 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_orderaddress_id_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('On hold', 'On hold'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded')], max_length=12, verbose_name='Estado'),
        ),
    ]