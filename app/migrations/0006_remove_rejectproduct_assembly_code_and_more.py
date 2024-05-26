# Generated by Django 5.0.6 on 2024-05-25 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_product_qty_assemblyproducts_product_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rejectproduct',
            name='assembly_code',
        ),
        migrations.RemoveField(
            model_name='rejectproduct',
            name='product_code',
        ),
        migrations.RemoveField(
            model_name='repairproduct',
            name='assembly_code',
        ),
        migrations.RemoveField(
            model_name='repairproduct',
            name='product_code',
        ),
        migrations.AddField(
            model_name='dispatchedproduct',
            name='dispatched_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='packagedproduct',
            name='packaged_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='rejectproduct',
            name='assembly',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.assemblyline', to_field='assembly_code'),
        ),
        migrations.AddField(
            model_name='rejectproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product', to_field='product_code'),
        ),
        migrations.AddField(
            model_name='repairproduct',
            name='assembly',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.assemblyline', to_field='assembly_code'),
        ),
        migrations.AddField(
            model_name='repairproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product', to_field='product_code'),
        ),
    ]