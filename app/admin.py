from django.contrib import admin
from app.models import (
    Product, 
    AssemblyLine, 
    AssemblyProducts,
    DailyInventory,
    PackagedProduct,
    DispatchedProduct,
    RepairProduct,
    RejectProduct 
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
    list_display = ('id','product','assembly','opening_stock','closing_stock','packaged_date')
admin.site.register(PackagedProduct, PackagedProductData)

class DispatchedProductData(admin.ModelAdmin):
    list_display = ('id','product','assembly','quantity','dispatched_date')
admin.site.register(DispatchedProduct, DispatchedProductData)

class RepairProductData(admin.ModelAdmin):
    list_display = ('id','product','assembly','opening_stock','closing_stock','date')
admin.site.register(RepairProduct, RepairProductData)

class RejectProductData(admin.ModelAdmin):
    list_display = ('id','product','assembly','quantity','date')
admin.site.register(RejectProduct, RejectProductData)