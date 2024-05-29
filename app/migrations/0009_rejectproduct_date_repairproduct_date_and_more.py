# Generated by Django 5.0.6 on 2024-05-28 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='rejectproduct',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='repairproduct',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='dailyinventory',
            name='inventory_date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='dispatchedproduct',
            name='dispatched_date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='packagedproduct',
            name='packaged_date',
            field=models.DateField(default=None),
        ),
    ]