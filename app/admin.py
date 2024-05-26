from django.contrib import admin
from app.models import (
    Product, 
    PackagedProduct, 
    AssemblyLine, 
    AssemblyProducts,
    DailyInventory
)


# Register your models here.

class ProductData(admin.ModelAdmin):
    list_display = ('product_id','product_code','product_name','product_description','product_quantity','product_status','created_at')
admin.site.register(Product, ProductData)


class AssemblyLineData(admin.ModelAdmin):
    list_display = ('id','assembly_code','assembly_name','status','created_at')
admin.site.register(AssemblyLine, AssemblyLineData)

class AssemblyProductsData(admin.ModelAdmin):
    list_display = ('id','assembly','product','product_quantity','status','created_at')
admin.site.register(AssemblyProducts, AssemblyProductsData)

class DailyInventoryData(admin.ModelAdmin):
    list_display = ('id','product','opening_stock','closing_stock','inventory_date')
admin.site.register(DailyInventory, DailyInventoryData)

class PackagedProductData(admin.ModelAdmin):
    list_display = ('id','product','assembly','quantity','created_at')
admin.site.register(PackagedProduct, PackagedProductData)