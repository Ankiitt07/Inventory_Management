from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    Users,
    Product, 
    AssemblyLine, 
    AssemblyProducts, 
    DailyInventory,
    PackagedProduct,
    DispatchedProduct,
    RepairProduct,
    RejectProduct
)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["email", "password", "first_name", "last_name"]
    
    def save(self):

        if Users.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "This email already exists!"})

        # Create the user with hashed password
        user = Users.objects.create(
            email=self.validated_data["email"],
            password=make_password(self.validated_data["password"]),
            first_name=self.validated_data.get("first_name", ""),
            last_name=self.validated_data.get("last_name", "")
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "product_id", 
            "product_code", 
            "product_name",
            "product_description",
            "product_quantity",
            "product_status",
            "created_at"
        ]
    
    def validate_product_code(self, value):
        if Product.objects.filter(product_code=value).exists():
            raise serializers.ValidationError("Product code already exists.")
        return value


class AssemblyLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssemblyLine
        fields = [
            "id", 
            "assembly_code", 
            "assembly_name",
            "status",
            "created_at"
        ]


class AssemblyProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssemblyProducts
        fields = [
            "id", 
            "assembly", 
            "product",
            "product_quantity",
            "status"
        ]


class DailyInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyInventory
        fields = [
            "id", 
            "product", 
            "opening_stock",
            "closing_stock",
            "inventory_date"
        ]
    
    def create(self, validated_data):
        validated_data['closing_stock'] = validated_data['opening_stock']
        return super().create(validated_data)


class PackagedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackagedProduct
        fields = [
            "id", 
            "product", 
            "assembly",
            "opening_stock",
            "closing_stock",
            "packaged_date"
        ]


class DispatchedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispatchedProduct
        fields = [
            "id", 
            "packaged_product", 
            "quantity",
            "dispatched_date"
        ]


class RepairProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairProduct
        fields = [
            "id", 
            "product", 
            "assembly",
            "quantity",
            "status",
            "date"
        ]


class RejectProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RejectProduct
        fields = [
            "id", 
            "product_code", 
            "assembly_code",
            "quantity",
            "created_at"
        ]