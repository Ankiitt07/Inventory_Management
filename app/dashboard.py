import pandas as pd
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from django.contrib import messages
from django.db.models import Sum
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .token_auth_helper import verify_token_class, generate_order_no

from .models import (
    PackagedProduct,
    DispatchedProduct,
    RepairProduct,
    RejectProduct
    )


class ProductsAnalytics(APIView):

    # @verify_token_class
    def get(self, request, format=None):
        current_date = date.today()

        # Calculate the first and last day of the current week
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Calculate the first and last day of the current month
        start_of_month = current_date.replace(day=1)
        if current_date.month == 12:
            end_of_month = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)

        # Daily data aggregation
        packaged_data_day = PackagedProduct.objects.filter(packaged_date=current_date).aggregate(Sum('opening_stock'))
        dispatched_data_day = DispatchedProduct.objects.filter(dispatched_date=current_date).aggregate(Sum('quantity'))
        repaired_data_day = RepairProduct.objects.filter(date=current_date).aggregate(Sum('opening_stock'))
        reject_data_day = RejectProduct.objects.filter(date=current_date).aggregate(Sum('quantity'))

        # Weekly data aggregation
        packaged_data_week = PackagedProduct.objects.filter(packaged_date__range=[start_of_week, end_of_week]).aggregate(Sum('opening_stock'))
        dispatched_data_week = DispatchedProduct.objects.filter(dispatched_date__range=[start_of_week, end_of_week]).aggregate(Sum('quantity'))
        repaired_data_week = RepairProduct.objects.filter(date__range=[start_of_week, end_of_week]).aggregate(Sum('opening_stock'))
        reject_data_week = RejectProduct.objects.filter(date__range=[start_of_week, end_of_week]).aggregate(Sum('quantity'))

        # Monthly data aggregation
        packaged_data_month = PackagedProduct.objects.filter(packaged_date__range=[start_of_month, end_of_month]).aggregate(Sum('opening_stock'))
        dispatched_data_month = DispatchedProduct.objects.filter(dispatched_date__range=[start_of_month, end_of_month]).aggregate(Sum('quantity'))
        repaired_data_month = RepairProduct.objects.filter(date__range=[start_of_month, end_of_month]).aggregate(Sum('opening_stock'))
        reject_data_month = RejectProduct.objects.filter(date__range=[start_of_month, end_of_month]).aggregate(Sum('quantity'))

        response = {
            "success": True,
            "message": "Packaging data",
            "date": current_date,
            "daily_data": {
                "packed_data": packaged_data_day,
                "dispatched_data": dispatched_data_day,
                "repaired_data": repaired_data_day,
                "reject_data": reject_data_day,
            },
            "weekly_data": {
                "packed_data": packaged_data_week,
                "dispatched_data": dispatched_data_week,
                "repaired_data": repaired_data_week,
                "reject_data": reject_data_week,
            },
            "monthly_data": {
                "packed_data": packaged_data_month,
                "dispatched_data": dispatched_data_month,
                "repaired_data": repaired_data_month,
                "reject_data": reject_data_month,
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class Invoice(APIView):
    
    @verify_token_class
    def post(self, request, format=None):
        product_data = request.data.get('product_data')

        order_no = generate_order_no()
        
