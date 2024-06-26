from django.urls import path, include
from .views import (
    ProductsData,
    AssemblyLineData,
    AssemblyProductData, 
    ProductListView, 
    UploadBulkProducts, 
    UploadAssembly, 
    UploadAssemblyProducts,
    AssemblyListView,
    AssemblyProductsListView,
    DailyInventoryData,
    PackagedProductData,
    DispatchedProductData,
    RepairedProductData,
    RejectProductData
)
from app import dashboard
from app.auth import (
    UserRegister, 
    UserLogin,
    Logout, 
    ResetPassword
)
from .views import add_opening_stocks
from app.token_auth_helper import generate_order_no

urlpatterns = [

    # URLs related to auth APIs
    path("user_register/", UserRegister.as_view(), name='user_register'),
    path("user_login/", UserLogin.as_view(), name='user_login'),
    path("user_logout/", Logout.as_view(), name='user_logout'),
    path("reset_password/", ResetPassword.as_view(), name='reset_password'),

    # URLs related to product data API.
    path("products_data/", ProductsData.as_view(), name='products_data'),

    # URLs related to assembly line data
    path("assembly_line_data/", AssemblyLineData.as_view(), name='assembly_line_data'),

    # URLs related to assembly product data API.
    path('assembly_product_data/', AssemblyProductData.as_view(), name='assembly_product_data'),

    # URLs related to daily inventory data API.
    path('daily_inventory_data/', DailyInventoryData.as_view(), name='daily_inventory_data'),
    
    # URLs related to packaged product data API.
    path('packaged_product_data/', PackagedProductData.as_view(), name='packaged_product_data'),
    
    # URLs related to dispatched product data API.
    path('dispatched_product_data/', DispatchedProductData.as_view(), name='dispatched_product_data'),

    # URLs related to dispatched product data API.
    path('repair_product_data/', RepairedProductData.as_view(), name='repair_product_data'),

    # URLs related to dispatched product data API.
    path('reject_product_data/', RejectProductData.as_view(), name='reject_product_data'),

    # URLs related to data via excel sheet
    path("upload_products_data/", UploadBulkProducts.as_view()),
    path("upload_assembly_data/", UploadAssembly.as_view()),
    path("upload_assembly_products/", UploadAssemblyProducts.as_view()),

    # URLs related to testing APIs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('assembly/', AssemblyListView.as_view(), name='assembly-list'),
    path('assembly_products/', AssemblyProductsListView.as_view(), name='assembly-products-list'),
    path('add_opening_stocks/', add_opening_stocks, name='add_opening_stocks'),


    # URLs for Analytics
    path(
        'products_count_data/<str:date>/', 
        dashboard.ProductsAnalytics.as_view({"get": "get_products_count"}), 
        name="get_products_count"
    ),
    path(
        'daily_products_count_data/', 
        dashboard.ProductsAnalytics.as_view({"get": "get_daily_products_count"}), 
        name="get_products_count"
    ),
    path(
        'dashboard_graph_data/', 
        dashboard.DashboardGraphData.as_view(), 
        name="dashboard_graph_data"
    ),

    # URLs for testing
    path('add_products/', add_opening_stocks, name='add_products'),
    path('generate_order_no/', generate_order_no, name='generate_order_no')    
]