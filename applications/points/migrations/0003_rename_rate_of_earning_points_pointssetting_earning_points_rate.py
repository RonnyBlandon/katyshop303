# Generated by Django 4.1.7 on 2023-05-26 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0002_pointshistory_id_order_alter_pointshistory_event_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pointssetting',
            old_name='rate_of_earning_points',
            new_name='earning_points_rate',
        ),
    ]