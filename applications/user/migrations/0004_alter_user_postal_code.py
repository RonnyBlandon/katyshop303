# Generated by Django 4.1.6 on 2023-02-05 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_unique_together_user_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Codigo Postal'),
        ),
    ]
