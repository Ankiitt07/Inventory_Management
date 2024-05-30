import pandas as pd
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from datetime import date, timedelta, datetime
from django.contrib import messages
from django.db.models import Sum, Count
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
    
    @verify_token_class
    def get_daily_products_count(self, request, format=None):

        current_date = date.today()

        inventory_serializer = DailyInventorySerializer(DailyInventory.objects.filter(inventory_date = current_date), many = True)
        package_serializer = PackagedProductSerializer(PackagedProduct.objects.filter(packaged_date = current_date), many = True)
        dispatch_serializer = DispatchedProductSerializer(DispatchedProduct.objects.filter(dispatched_date = current_date), many = True)
        repair_serializer = RepairProductSerializer(RepairProduct.objects.filter(date = current_date), many = True)
        reject_serializer = RejectProductSerializer(RejectProduct.objects.filter(date = current_date), many = True)

        
        response = {
            "success": True,
            "message": "Analytics data fetched",
            "date": current_date,
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


class DashboardGraphData(APIView):

    @verify_token_class
    def get(self, request, format=None):
        response = {
            "success": True,
            "message": "success",
            "weekly":{
                "series_weekly" : self.get_weekly_data(),
                "categories_weekly": self.get_weekly_categories(),
            }, 
            "monthly":{
                "series_monthly" : self.get_monthly_data(),
                "categories_monthly": self.get_weekly_categories(),
            } 
        }
        return Response(response, status=status.HTTP_200_OK)

    def get_weekly_data(self):
        today = date.today()
        seven_days_ago = today - timedelta(days=7)
        dates = [seven_days_ago + timedelta(days=i) for i in range(7)]

        def get_closing_stock_sum_weekly(model, date_field):
            closing_stock_sum = []
            for current_date in dates:
                daily_data = model.objects.filter(**{date_field: current_date})
                if model in (DispatchedProduct, RejectProduct):
                    total_closing_stock = daily_data.aggregate(total=Sum('quantity'))['total']
                else:
                    total_closing_stock = daily_data.aggregate(total=Sum('closing_stock'))['total']
                closing_stock_sum.append(total_closing_stock or 0)
            return closing_stock_sum

        inventory_data = get_closing_stock_sum_weekly(DailyInventory, 'inventory_date')
        packaging_data = get_closing_stock_sum_weekly(PackagedProduct, 'packaged_date')
        dispatch_data = get_closing_stock_sum_weekly(DispatchedProduct, 'dispatched_date')
        repair_data = get_closing_stock_sum_weekly(RepairProduct, 'date')
        reject_data = get_closing_stock_sum_weekly(RejectProduct, 'date')

        return [
            {
                "name": "Inventory",
                "data": inventory_data,
            },
            {
                "name": "Packaging",
                "data": packaging_data,
            },
            {
                "name": "Dispatch",
                "data": dispatch_data,
            },
            {
                "name": "Repair",
                "data": repair_data,
            },
            {
                "name": "Reject",
                "data": reject_data,
            },
        ]

    def get_monthly_data(self):
        today = date.today()
        start_of_month = today.replace(day=1)

        def get_closing_stock_sum_monthly(model, date_field):
            monthly_data = model.objects.filter(**{f'{date_field}__range': [start_of_month, today]})
            if model in (DispatchedProduct, RejectProduct):
                total_closing_stock = monthly_data.aggregate(total=Sum('quantity'))['total']
            else:
                total_closing_stock = monthly_data.aggregate(total=Sum('closing_stock'))['total']
            return total_closing_stock or 0

        inventory_data = get_closing_stock_sum_monthly(DailyInventory, 'inventory_date')
        packaging_data = get_closing_stock_sum_monthly(PackagedProduct, 'packaged_date')
        dispatch_data = get_closing_stock_sum_monthly(DispatchedProduct, 'dispatched_date')
        repair_data = get_closing_stock_sum_monthly(RepairProduct, 'date')
        reject_data = get_closing_stock_sum_monthly(RejectProduct, 'date')

        return [
            {
                "name": "Inventory",
                "data": [inventory_data],
            },
            {
                "name": "Packaging",
                "data": [packaging_data],
            },
            {
                "name": "Dispatch",
                "data": [dispatch_data],
            },
            {
                "name": "Repair",
                "data": [repair_data],
            },
            {
                "name": "Reject",
                "data": [reject_data],
            },
        ]

    def get_weekly_categories(self):
        today = date.today()
        seven_days_ago = today - timedelta(days=7)
        dates = [seven_days_ago + timedelta(days=i) for i in range(7)]
        return [date.strftime("%A") for date in dates]