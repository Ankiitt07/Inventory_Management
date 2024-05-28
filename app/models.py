from django.db import models

# Create your models here.

status_choice = [
    (0, 'Inactive'),
    (1, 'Active')
]


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250, default=None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    soft_deleted = models.IntegerField(default=0)

    def __str__(self):
            return self.first_name

    class Meta:
        db_table = 'users_table'
        managed = True


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=200, unique=True)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    product_status = models.IntegerField(
        choices=status_choice,
        default=1
    )
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'product_table'
        managed = True


class AssemblyLine(models.Model):
    id = models.AutoField(primary_key=True)
    assembly_code = models.CharField(max_length=200, unique=True)
    assembly_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(
        choices=status_choice,
        default=1
    )
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.assembly_name
    
    class Meta:
        db_table = 'assembly_line_table'
        managed = True


class AssemblyProducts(models.Model):
    id = models.AutoField(primary_key=True)
    assembly = models.ForeignKey(AssemblyLine, to_field="assembly_code", on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, to_field="product_code", on_delete=models.CASCADE, blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(
        choices=status_choice,
        default=1
    )
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.assembly.assembly_code
    
    class Meta:
        db_table = 'assembly_product_table'
        managed = True


class DailyInventory(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, to_field="product_code", on_delete=models.CASCADE, default=None)
    opening_stock = models.IntegerField(default=0)
    closing_stock = models.IntegerField(default=0)
    inventory_date = models.DateField(default = None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.product.product_code
    
    class Meta:
        db_table = 'daily_inventory_table'
        managed = True


class PackagedProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, to_field="product_code", on_delete=models.CASCADE, blank=True, null=True)
    assembly = models.ForeignKey(AssemblyLine, to_field="assembly_code", on_delete=models.CASCADE, blank=True, null=True)
    opening_stock = models.IntegerField(default=0)
    closing_stock = models.IntegerField(default=0)
    packaged_date = models.DateField(default = None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'pakaged_product_table'
        managed = True


class DispatchedProduct(models.Model):
    id = models.AutoField(primary_key=True)
    packaged_product = models.ForeignKey(PackagedProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dispatched_date = models.DateField(default = None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.packaged_product
    
    class Meta:
        db_table = 'dispatched_product_table'
        managed = True


class RepairProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, to_field="product_code", on_delete=models.CASCADE, blank=True, null=True)
    assembly = models.ForeignKey(AssemblyLine, to_field="assembly_code", on_delete=models.CASCADE, blank=True, null=True)
    opening_stock = models.IntegerField(default=0)
    closing_stock = models.IntegerField(default=0)
    status = models.IntegerField(
        choices=status_choice,
        default=1
    )
    date = models.DateField(default = None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'repair_product_table'
        managed = True


class RejectProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, to_field="product_code", on_delete=models.CASCADE, blank=True, null=True)
    assembly = models.ForeignKey(AssemblyLine, to_field="assembly_code", on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    date = models.DateField(default = None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'reject_product_table'
        managed = True