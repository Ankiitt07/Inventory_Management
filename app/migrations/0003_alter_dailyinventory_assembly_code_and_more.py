# Generated by Django 5.0.6 on 2024-05-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_assemblyproducts_assembly_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyinventory',
            name='assembly_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='dailyinventory',
            name='product_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='packagedproduct',
            name='assembly_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='packagedproduct',
            name='product_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rejectproduct',
            name='assembly_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rejectproduct',
            name='product_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='repairproduct',
            name='assembly_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='repairproduct',
            name='product_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
