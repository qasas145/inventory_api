from django.contrib import admin
from .models import InventoryGroup, Inventory, Invoice, InvoiceItem, Shop


admin.site.register(InventoryGroup)
admin.site.register(Inventory)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Shop)




# Register your models here.
