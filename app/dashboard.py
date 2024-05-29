import pandas as pd
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from datetime import date, timedelta
from django.contrib import messages
from django.db.models import Sum
from .models import Product, InvoiceData, InvoiceProducts
from .serializers import (
    DailyInventorySerializer,
    PackagedProductSerializer,
    DispatchedProductSerializer,
    RepairProductSerializer,
    RejectProductSerializer,
    InvoiceProductSerializer
    )
from django.shortcuts import render, redirect, get_object_or_404
from .token_auth_helper import verify_token_class, generate_order_no

from .models import (
    DailyInventory,
    PackagedProduct,
    DispatchedProduct,
    RepairProduct,
    RejectProduct
    )


class ProductsAnalytics(viewsets.ModelViewSet):

    @verify_token_class
    def get_products_count(self, request, date, format=None):

        inventory_serializer = DailyInventorySerializer(DailyInventory.objects.filter(inventory_date = date), many = True)
        package_serializer = PackagedProductSerializer(PackagedProduct.objects.filter(packaged_date = date), many = True)
        dispatch_serializer = DispatchedProductSerializer(DispatchedProduct.objects.filter(dispatched_date = date), many = True)
        repair_serializer = RepairProductSerializer(RepairProduct.objects.filter(date = date), many = True)
        reject_serializer = RejectProductSerializer(RejectProduct.objects.filter(date = date), many = True)

        
        response = {
            "success": True,
            "message": "Analytics data fetched",
            "date": date,
            "inventory_data": inventory_serializer.data,
            "package_data": package_serializer.data,
            "dispatch_data": dispatch_serializer.data,
            "repair_data": repair_serializer.data,
            "reject_data": reject_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class Invoice(APIView):
    
    @verify_token_class
    def post(self, request, format=None):

        product_data = request.data.get('product_data')
        assembly_data = request.data.get('assembly_data')
        total_amount = request.data.get('total_amount')

        order_no = generate_order_no()

        if order_no:
            try:
                InvoiceData.objects.create(
                    order_no = order_no,
                    total_amount = total_amount,
                    date =  date.today()
                )
            except Exception as e:
                return Response({"error" : f"{e}"})
        
        invoice_products = []
        if product_data:
            for data in product_data:
                item = {
                    "order_no" : order_no,
                    "product" : data['product'],
                    "quantity" : data['quantity'],
                    "date" :  date.today()
                }
                invoice_products.append(item)
        if assembly_data:
            for data in assembly_data:
                item = {
                    "order_no" : order_no,
                    "assembly" : data['assembly'],
                    "quantity" : data['quantity'],
                    "date" :  date.today()
                }
                invoice_products.append(item)
        serializer = InvoiceProductSerializer(invoice_products, many=True)

        if serializer.is_valid():
            serializer.save()
            response = {
                "success" : True,
                "message" : "Invoice product addedd successfully",
                "data" : {"invoive_data" : serializer.data}
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)