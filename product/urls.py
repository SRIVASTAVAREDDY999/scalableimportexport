from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-product/', views.create_product, name='create_product'),
    path('update-product/', views.update_product, name='update_product'),
    path('delete-product/', views.delete_product, name='delete_product'),
    path('view-products/', views.view_products, name='view_products'),
    path('view-external-products/', views.view_external_products, name='view_external_products'),
    path('generate-otp/', views.generate_otp, name='generate_otp'),
    path('debug-products/', views.debug_products, name='debug_products'),
]
