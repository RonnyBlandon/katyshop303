# Generated by Django 4.1.6 on 2023-02-05 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Dirección'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Ciudad'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Pais'),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='user',
            name='validation_code',
            field=models.CharField(max_length=6, verbose_name='Código de Validación'),
        ),
    ]
