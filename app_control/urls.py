from django.contrib import admin
from django.urls import path, include
from .views import InventoryGroupView, InventoryView, PurchaseView, SaleByShopView, ShopView, InvoiceView, InvoiceItemView, SalePerformanceView
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register("inventory", InventoryView)
router.register("inventory-group", InventoryGroupView)
router.register("shop", ShopView)
router.register("invoice", InvoiceView)
router.register("invoice-item", InvoiceItemView)
router.register("sale-performance", SalePerformanceView)
router.register('sales-by-shop', SaleByShopView, "sales-by-shop")
router.register('purchase-summary', PurchaseView, "purchase-summary")
urlpatterns = [
    path("", include(router.urls)),
]
