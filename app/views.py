import pandas as pd
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date, timedelta
from django.shortcuts import render, get_object_or_404
from .token_auth_helper import verify_token_class
from .models import (
    Product, 
    AssemblyLine, 
    AssemblyProducts, 
    DailyInventory,
    PackagedProduct,
    DispatchedProduct,
    RepairProduct,
    RejectProduct
    )

from .serializers import (
    ProductSerializer,
    AssemblyLineSerializer,
    AssemblyProductSerializer,
    DailyInventorySerializer,
    PackagedProductSerializer,
    DispatchedProductSerializer,
    RepairProductSerializer,
    RejectProductSerializer
    )
from django.views.generic import ListView

# Create your views here.


class ProductsData(APIView):

    @verify_token_class
    def get(self, request, format=None):
        
        product_data = Product.objects.filter(product_status = 1)

        serializer = ProductSerializer(product_data, many = True)

        response = {
            "success" : True,
            "message" : "Product Data Fetched Successfully",
            "data" : {"products": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @verify_token_class
    def post(self, request, format=None):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "success" : True,
                "message" : "Product Data addedd successfully",
                "data" : {"product" : serializer.data}
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @verify_token_class
    def patch(self, request, format=None):

        product_instance = get_object_or_404(Product, product_code = request.data.get("product_code"))
        
        serializer = ProductSerializer(product_instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "message": "Product Data updated successfully",
                "data": {"product": serializer.data}
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssemblyLineData(APIView):

    @verify_token_class
    def get(self, request, format=None):
        
        assembly_line_data = AssemblyLine.objects.all()

        serializer = AssemblyLineSerializer(assembly_line_data, many = True)

        response = {
            "success" : True,
            "message" : "Assembly Line Data Fetched Successfully",
            "data" : {"assembly_line": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @verify_token_class
    def post(self, request, format=None):

        serializer = AssemblyLineSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "success" : True,
                "message" : "Assembly line addedd successfully",
                "data" : {"product" : serializer.data}
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @verify_token_class
    def patch(self, request, format=None):

        product_instance = get_object_or_404(Product, product_code = request.data.get("product_code"))
        
        serializer = ProductSerializer(product_instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "message": "Product Data updated successfully",
                "data": {"product": serializer.data}
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssemblyProductData(APIView):

    @verify_token_class
    def get(self, request, format=None):
        
        assembly_product_data = AssemblyProducts.objects.filter(assembly__assembly_code = "ALCA077A")

        serializer = AssemblyProductSerializer(assembly_product_data, many = True)

        response = {
            "success" : True,
            "message" : "Assembly Line Data Fetched Successfully",
            "data" : {"assembly_products": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @verify_token_class
    def post(self, request, format=None):

        serializer = AssemblyLineSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "success" : True,
                "message" : "Product addedd successfully",
                "data" : {"product" : serializer.data}
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadBulkProducts(APIView):
    
    @verify_token_class
    def post(self, request, format=None):

        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No product file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                Product.objects.create(
                    product_code=row['product_code'],
                    product_name=row['product_name'],
                    product_description=row['product_description'],
                )
            return Response({"message": "Product Data uploaded successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadAssembly(APIView):
    
    @verify_token_class
    def post(self, request, format=None):

        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                AssemblyLine.objects.create(
                    assembly_code=row['assembly_code'],
                    assembly_name=row['assembly_name'],
                )
            return Response({"message": "Assembly Data uploaded successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadAssemblyProducts(APIView):
    
    @verify_token_class
    def post(self, request, format=None):

        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        df = pd.read_excel(excel_file)
        assembly_products = []
        for index, row in df.iterrows():
            item = {
                "assembly" : row['assembly'],
                "product" :  row['product'],
                "product_quantity" : row['product_quantity']
            }
            assembly_products.append(item)
        serializer = AssemblyProductSerializer(data=assembly_products, many=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success" : True,
                "message" : "Assembly Products Addedd Successfully",
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/products_list.html'
    context_object_name = 'products'


class AssemblyListView(ListView):
    model = AssemblyLine
    template_name = 'dashboard/assembly_line.html'
    context_object_name = 'assembly_line'


class AssemblyProductsListView(ListView):

    model = AssemblyProducts
    template_name = 'dashboard/assembly_products_list.html'
    context_object_name = 'assembly_products'



def add_opening_stocks(request):

    products = Product.objects.all()

    return render(request, "dashboard/add_opening_stocks.html", {'products' : products})


class DailyInventoryData(APIView):

    @verify_token_class
    def get(self, request, format=None):

        current_date = date.today()
        print(current_date)

        inventory_data = DailyInventory.objects.filter(inventory_date = current_date)

        serializer = DailyInventorySerializer(inventory_data, many = True)

        response = {
            "success" : True,
            "message" : "Daily Inventory Data Fetched Successfully",
            "data" : {"inventory_data": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)

    @verify_token_class
    def post(self, request, format=None):

        inventory_data = request.data.get('inventory_data')

        updated_inventory_data = []
        current_date = date.today()
        for data in inventory_data:
            current_date_inventory = DailyInventory.objects.filter(product_id = data['product'], inventory_date = current_date).first()
            if current_date_inventory:
                current_date_inventory.opening_stock += int(data['opening_stock'])
                current_date_inventory.closing_stock += int(data['opening_stock'])
                current_date_inventory.save()
            else:
                last_inventory = DailyInventory.objects.filter(product_id = data['product']).order_by('-inventory_date').first()
                if last_inventory and last_inventory.closing_stock != 0:
                    opening_stock = int(last_inventory.closing_stock) + int(data['opening_stock'])
                    last_inventory.closing_stock = 0
                    last_inventory.save()
                else:
                    opening_stock = int(data['opening_stock'])
                item = {
                    "product" : data['product'],
                    "opening_stock" :opening_stock,
                    "inventory_date" : current_date
                }
                updated_inventory_data.append(item)
       
        if updated_inventory_data:
            serializer = DailyInventorySerializer(data=updated_inventory_data, many=True)

            if serializer.is_valid():

                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success" : "addedd successfully"}, status=status.HTTP_200_OK)


class PackagedProductData(APIView):

    @verify_token_class
    def get(self, request, format=None):
        
        current_date = date.today()
        packaged_product_data = PackagedProduct.objects.filter(packaged_date = current_date)

        serializer = PackagedProductSerializer(packaged_product_data, many = True)

        response = {
            "success" : True,
            "message" : "Pakaged Product Data Fetched Successfully",
            "data" : {"pakaged_products": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)


    @verify_token_class
    def post(self, request, format=None):
        product_data = request.data.get('product_data')
        assembly_data = request.data.get('assembly_data')

        if product_data:
            response = self.handle_product_data(product_data)
            if response:
                return response

        if assembly_data:
            response = self.handle_assembly_data(assembly_data)
            if response:
                return response

        response = {
            "success": True,
            "message": "Packaged Products Added successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def handle_product_data(self, product_data):
        try:
            with transaction.atomic():
                for data in product_data:
                    product_code = data['product']
                    quantity = int(data['quantity'])
                    
                    product_data = self.get_daily_inventory(product_code)
                    if not product_data:
                        return self.not_found_response(product_code)
                    
                    if product_data.closing_stock < quantity:
                        return self.insufficient_stock_response(product_code)
                    
                    self.update_closing_stock_for_product_from_inventory(product_data, quantity)
                    self.create_or_update_packaged_product(product_code, quantity)
        except Exception as e:
            return self.error_response(e)
    
    def handle_assembly_data(self, assembly_data):
        try:
            with transaction.atomic():
                for data in assembly_data:
                    assembly = data['assembly']
                    assembly_quantity = int(data['quantity'])
                    
                    assembly_product_data = AssemblyProducts.objects.filter(assembly__assembly_code=assembly)
                    
                    for item in assembly_product_data:
                        product_code = item.product.product_code
                        product_quantity = item.product_quantity
                        
                        product_data = self.get_daily_inventory(product_code)
                        if not product_data:
                            return self.not_found_response(product_code)
                        
                        if product_data.closing_stock < product_quantity*assembly_quantity:
                            return self.insufficient_stock_response_for_assembly(product_code, assembly)
                        
                        self.update_closing_stock_for_assembly_from_inventory(product_data, product_quantity, assembly_quantity)
                    
                    self.create_or_update_packaged_product_for_assembly(assembly, assembly_quantity)

        except Exception as e:
            return self.error_response(e)
    
    def get_daily_inventory(self, product_code):
        try:
            current_date = date.today()
            return DailyInventory.objects.get(product__product_code=product_code, inventory_date = current_date)
        except DailyInventory.DoesNotExist:
            return None
    
    def update_closing_stock_for_product_from_inventory(self, product_data, product_quantity):
        product_data.closing_stock -= product_quantity
        product_data.save()
    
    def update_closing_stock_for_assembly_from_inventory(self, product_data, product_quantity, assembly_quantity):
        product_data.closing_stock -= product_quantity*assembly_quantity
        product_data.save()
    
    def create_or_update_packaged_product(self, product_code, quantity):
        today = date.today()
        packaged_product = PackagedProduct.objects.filter(product_id=product_code, packaged_date=today).first()
        if packaged_product:
            packaged_product.opening_stock += quantity
            packaged_product.closing_stock += quantity
            packaged_product.save()
        
            return packaged_product, False
        else:
            last_package = PackagedProduct.objects.filter(product_id = product_code).order_by('-packaged_date').first()
            if last_package and last_package.closing_stock != 0:
                update_opening_stock = int(last_package.closing_stock) + int(quantity)
            else:
                update_opening_stock = int(quantity)
            packaged_product = PackagedProduct.objects.create(
                product_id=product_code, opening_stock=update_opening_stock, closing_stock=update_opening_stock,packaged_date=today
            )
            return packaged_product, True 
    
    def create_or_update_packaged_product_for_assembly(self, assembly, assembly_quantity):
        today = date.today()
        packaged_product = PackagedProduct.objects.filter(assembly_id=assembly, packaged_date=today).first()
        if packaged_product:
            packaged_product.opening_stock += assembly_quantity
            packaged_product.closing_stock += assembly_quantity
            packaged_product.save()
            
            return packaged_product, False
        else:
            last_assembly = PackagedProduct.objects.filter(assembly_id=assembly).order_by('-packaged_date').first()
            if last_assembly and last_assembly.closing_stock != 0:
                update_opening_stock = int(last_assembly.closing_stock) + int(assembly_quantity)
            else:
                update_opening_stock = int(assembly_quantity)

            packaged_product = PackagedProduct.objects.create(assembly_id=assembly, opening_stock=update_opening_stock, closing_stock=update_opening_stock, packaged_date=today)
            return packaged_product, True 

    def not_found_response(self, product_code):
        response = {
            "success": False,
            "message": f"DailyInventory for product code {product_code} does not exist"
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    def insufficient_stock_response(self, product_code):
        response = {
            "success": False,
            "message": f"Required quantity for {product_code} is not in stock"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def insufficient_stock_response_for_assembly(self, product_code, assembly):
        response = {
            "success": False,
            "message": f"Required quantity of {product_code} for requested quantity of assembly line {assembly} is not in stock"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def error_response(self, error):
        response = {
            "success": False,
            "message": str(error)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DispatchedProductData(APIView):

    @verify_token_class
    def get(self, request, format=None):

        current_date = date.today()
        dispatched_product_data = DispatchedProduct.objects.filter(dispatched_date=current_date)

        serializer = DispatchedProductSerializer(dispatched_product_data, many = True)

        response = {
            "success" : True,
            "message" : "Dispatched Product Data Fetched Successfully",
            "data" : {"dispatched_product": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @verify_token_class
    def post(self, request, format=None):

        requested_data = request.data.get('packed_data')
        current_date = date.today()

        for data in requested_data:

            packed_product = PackagedProduct.objects.get(id = data['packaged_product'])
            dispatch_data = DispatchedProduct.objects.filter(packaged_product_id=data["packaged_product"])

            if packed_product.quantity < int(data['quantity']):
                response = {
                    "success": False,
                    "message": f"Required quantity for packed product is not in stock"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            elif dispatch_data.exists():
                dispatch_data_item = DispatchedProduct.objects.get(packaged_product_id=data["packaged_product"])
                dispatch_data_item.quantity += int(data['quantity'])
                dispatch_data_item.dispatched_date = current_date
                dispatch_data_item.save()
                packed_product.quantity = packed_product.quantity - int(data['quantity'])
                packed_product.save()

            else:
                DispatchedProduct.objects.create(
                    packaged_product_id=data["packaged_product"],
                    quantity = int(data['quantity']),
                    dispatched_date = current_date
                )
                packed_product.quantity = packed_product.quantity - int(data['quantity'])
                packed_product.save()
        
        response = {
            "success" : True,
            "message" : "Dispatch Product Added Successfully",
        }
        return Response(response, status=status.HTTP_200_OK)


class RepairedProductData(APIView):

    @verify_token_class
    def get(self, request, format=None):

        current_date = date.today()
        repaired_product_data = RepairProduct.objects.filter(date = current_date)

        serializer = RepairProductSerializer(repaired_product_data, many = True)

        response = {
            "success" : True,
            "message" : "Repair Product Data Fetched Successfully",
            "data" : {"repaired_product": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @verify_token_class
    def post(self, request, format=None):
        product_data = request.data.get('product_data')
        assembly_data = request.data.get('assembly_data')

        if product_data:
            response = self.handle_product_data(product_data)
            if response:
                return response

        if assembly_data:
            response = self.handle_assembly_data(assembly_data)
            if response:
                return response

        response = {
            "success": True,
            "message": "Products for repairing addedd successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def handle_product_data(self, product_data):
        try:
            with transaction.atomic():
                for data in product_data:
                    product_code = data['product']
                    quantity = int(data['quantity'])
                    
                    packed_product_data = self.get_product_packed_data(product_code)
                    if not product_data:
                        return self.not_found_response(product_code)
                    
                    if packed_product_data.quantity < quantity:
                        return self.insufficient_stock_response(product_code)
                    
                    self.update_quantity_for_product_in_packaging(packed_product_data, quantity)
                    self.create_or_update_repair_product(product_code, quantity)
        except Exception as e:
            return self.error_response(e)
    
    def handle_assembly_data(self, assembly_data):
        try:
            with transaction.atomic():
                for data in assembly_data:
                    assembly = data['assembly']
                    assembly_quantity = int(data['quantity'])
                        
                    packed_assembly_data = self.get_assembly_packed_data(assembly)
                    if not packed_assembly_data:
                        return self.not_found_response(assembly)
                    
                    if packed_assembly_data.quantity < assembly_quantity:
                        return self.insufficient_stock_response_for_assembly(assembly)
                    
                    self.update_quantity_for_assembly_in_packaging(packed_assembly_data, assembly_quantity)
                
                self.create_or_update_repair_product_for_assembly(assembly, assembly_quantity)

        except Exception as e:
            return self.error_response(e)
    
    def get_product_packed_data(self, product_code):
        try:
            current_date = date.today()
            return PackagedProduct.objects.get(product__product_code=product_code, packaged_date = current_date)
        except PackagedProduct.DoesNotExist:
            return None
    
    def get_assembly_packed_data(self, assembly):
        try:
            current_date = date.today()
            return PackagedProduct.objects.get(assembly__assembly_code=assembly, packaged_date = current_date)
        except PackagedProduct.DoesNotExist:
            return None
    
    def update_quantity_for_product_in_packaging(self, product_data, product_quantity):
        product_data.closing_stock -= product_quantity
        product_data.save()
    
    def update_quantity_for_assembly_in_packaging(self, packed_assembly_data, assembly_quantity):
        packed_assembly_data.quantity -= assembly_quantity
        packed_assembly_data.save()
    
    def create_or_update_repair_product(self, product_code, quantity):
    
        today = date.today()
        repair_product = RepairProduct.objects.filter(product_id=product_code, date=today).first()
        if repair_product:
            repair_product.opening_stock += quantity
            repair_product.closing_stock += quantity
            repair_product.save()
        
            return repair_product, False
        else:
            last_repair_product = RepairProduct.objects.filter(product_id = product_code).order_by('-date').first()
            if last_repair_product and last_repair_product.closing_stock != 0:
                update_opening_stock = int(last_repair_product.closing_stock) + int(quantity)
            else:
                update_opening_stock = int(quantity)
            packaged_product = RepairProduct.objects.create(
                product_id=product_code, opening_stock=update_opening_stock, closing_stock=update_opening_stock,packaged_date=today
            )
            return packaged_product, True
    
    def create_or_update_repair_product_for_assembly(self, assembly, assembly_quantity):

        today = date.today()
        repair_product = RepairProduct.objects.filter(assembly_id=assembly, date=today).first()
        if repair_product:
            repair_product.opening_stock += assembly_quantity
            repair_product.closing_stock += assembly_quantity
            repair_product.save()
            
            return repair_product, False
        else:
            last_repair_assembly = RepairProduct.objects.filter(assembly_id=assembly).order_by('-date').first()
            if last_repair_assembly and last_repair_assembly.closing_stock != 0:
                update_opening_stock = int(last_repair_assembly.closing_stock) + int(assembly_quantity)
            else:
                update_opening_stock = int(assembly_quantity)
            assembly_product = RepairProduct.objects.create(
                assembly_id=assembly, opening_stock=update_opening_stock, closing_stock=update_opening_stock, packaged_date=today
            )
            return assembly_product, True

    def not_found_response(self, product_code):
        response = {
            "success": False,
            "message": f"Packaged Data for product code {product_code} does not exist"
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    def insufficient_stock_response(self, product_code):
        response = {
            "success": False,
            "message": f"Required quantity for {product_code} is not in packaged stock"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def insufficient_stock_response_for_assembly(self, assembly):
        response = {
            "success": False,
            "message": f"Required quantity of {assembly} is not in packaged stock"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def error_response(self, error):
        response = {
            "success": False,
            "message": str(error)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RejectProductData(APIView):


    @verify_token_class
    def get(self, request, format=None):
        
        current_date = date.today()
        reject_product_data = RejectProduct.objects.filter(date = current_date)

        serializer = RejectProductSerializer(reject_product_data, many = True)

        response = {
            "success" : True,
            "message" : "Reject Product Data Fetched Successfully",
            "data" : {"reject_product": serializer.data}
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @verify_token_class
    def post(self, request, format=None):
        product_data = request.data.get('product_data')
        assembly_data = request.data.get('assembly_data')

        if product_data:
            response = self.handle_product_data(product_data)
            if response:
                return response

        if assembly_data:
            response = self.handle_assembly_data(assembly_data)
            if response:
                return response

        response = {
            "success": True,
            "message": "Rejected Products addedd successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def handle_product_data(self, product_data):
        try:
            with transaction.atomic():
                for data in product_data:
                    product_code = data['product']
                    quantity = int(data['quantity'])
                    
                    packed_product_data = self.get_product_packed_data(product_code)
                    if not product_data:
                        return self.not_found_response(product_code)
                    
                    if packed_product_data.quantity < quantity:
                        return self.insufficient_stock_response(product_code)
                    
                    self.update_quantity_for_product(packed_product_data, quantity)
                    self.create_or_update_reject_product(product_code, quantity)
        except Exception as e:
            return self.error_response(e)
    
    def handle_assembly_data(self, assembly_data):
        try:
            with transaction.atomic():
                for data in assembly_data:
                    assembly = data['assembly']
                    assembly_quantity = int(data['quantity'])
                        
                    packed_assembly_data = self.get_assembly_packed_data(assembly)
                    if not packed_assembly_data:
                        return self.not_found_response(assembly)
                    
                    if packed_assembly_data.quantity < assembly_quantity:
                        return self.insufficient_stock_response_for_assembly(assembly)
                    
                    self.update_quantity_for_assembly(packed_assembly_data, assembly_quantity)
                
                self.create_or_update_reject_product_for_assembly(assembly, assembly_quantity)

        except Exception as e:
            return self.error_response(e)
    
    def get_product_packed_data(self, product_code):
        try:
            current_date = date.today()
            return PackagedProduct.objects.get(product__product_code=product_code, packaged_date = current_date)
        except PackagedProduct.DoesNotExist:
            return None
    
    def get_assembly_packed_data(self, assembly):
        try:
            current_date = date.today()
            return PackagedProduct.objects.get(assembly__assembly_code=assembly, packaged_date = current_date)
        except PackagedProduct.DoesNotExist:
            return None
    
    def update_quantity_for_product(self, product_data, product_quantity):
        product_data.quantity -= product_quantity
        product_data.save()
    
    def update_quantity_for_assembly(self, packed_assembly_data, assembly_quantity):
        packed_assembly_data.quantity -= assembly_quantity
        packed_assembly_data.save()
    
    def create_or_update_reject_product(self, product_code, quantity):
        try:
            today = date.today()
            reject_product = RejectProduct.objects.get(product_id=product_code, date=today)
            
            reject_product.quantity += quantity
            reject_product.save()
            
            return reject_product, False
        except RejectProduct.DoesNotExist:
            reject_product = RejectProduct.objects.create(product_id=product_code, quantity=quantity, date=today)
            return reject_product, True 
    
    def create_or_update_reject_product_for_assembly(self, assembly, assembly_quantity):
        try:
            today = date.today()
            reject_product = RejectProduct.objects.get(assembly_id=assembly, date=today)
            
            reject_product.quantity += assembly_quantity
            reject_product.save()
            
            return reject_product, False
        except RepairProduct.DoesNotExist:
            reject_product = RepairProduct.objects.create(assembly_id=assembly, quantity=assembly_quantity, date=today)
            return reject_product, True

    def not_found_response(self, product_code):
        response = {
            "success": False,
            "message": f"Packaged Data for product code {product_code} does not exist"
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    def insufficient_stock_response(self, product_code):
        response = {
            "success": False,
            "message": f"Required quantity for {product_code} is not in packaged stock"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def insufficient_stock_response_for_assembly(self, assembly):
        response = {
            "success": False,
            "message": f"Required quantity of {assembly} is not in packaged stock"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def error_response(self, error):
        response = {
            "success": False,
            "message": str(error)
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
