from rest_framework import serializers
from user_control.models import CustomUser
from user_control.serializer import CustomUserSerializer
from .models import InventoryGroup, Invoice, InvoiceItem, Shop, Inventory

class InventoryGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    belongs_to = serializers.SerializerMethodField(read_only=True)
    belongs_to_id = serializers.CharField(write_only=True, required=False)
    total_items = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = InventoryGroup
        fields = "__all__"


    def get_belongs_to(self, obj):
        if obj.belongs_to is not None:
            return InventoryGroupSerializer(obj.belongs_to).data
        return None




class InventorySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    group = InventoryGroupSerializer(read_only=True)
    group_id = serializers.CharField(write_only=True)

    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryWithSumSerializer(InventorySerializer):
    sum_of_item = serializers.IntegerField()

    
class ShopSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    amount_total = serializers.CharField(read_only=True, required=False)
    count_total = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Shop
        fields = "__all__"


class ShopWithAmountSerializer(ShopSerializer):
    amount_total = serializers.FloatField()
    month = serializers.CharField(required=False)


class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.CharField(read_only=True)
    invoice_id = serializers.CharField(write_only=True)
    item = InventorySerializer(read_only=True)
    item_id = serializers.CharField(write_only=True)

    class Meta:
        model = InvoiceItem
        fields = "__all__"

    def save(self, **kwargs):
        return super().save(**kwargs)


class InvoiceItemDataSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    quantity = serializers.IntegerField()



class InvoiceSerializer(serializers.ModelSerializer) :
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    shop = ShopSerializer(read_only=True)
    shop_id = serializers.CharField(write_only=True)

    invoice_items = InvoiceItemSerializer(many=True, read_only=True)

    invoice_item_data = InvoiceItemDataSerializer(write_only=True, many=True, required = False)

    class Meta:
        model = Invoice
        fields = "__all__"





    def create(self, validated_data):
        
        invoice_item_data = validated_data.pop("invoice_item_data")
        invoice = super().create(validated_data)
        if invoice_item_data :
            print(invoice_item_data)
            serializer = InvoiceItemSerializer(data=[
            {"invoice_id" : invoice.id,**item} for item in invoice_item_data], many = True)
            if not serializer.is_valid() :
                invoice.delete()
                print(serializer.errors)
            print(serializer.data)
            serializer.save()
        
        return invoice
