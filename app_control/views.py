from datetime import datetime
import queue
from django.shortcuts import render
from django.db.models.functions import Coalesce, TruncMonth

from django.db.models import Count, Sum, F

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from user_control.permissions import IsAuthenticatedCustom
from .serializer import InventoryGroupSerializer, InventorySerializer, InventoryWithSumSerializer, InvoiceSerializer, ShopSerializer, InvoiceItemSerializer, ShopWithAmountSerializer
from .models import Inventory, InventoryGroup, Invoice, InvoiceItem, Shop
from me_inventory.utils import CustomPagination, get_query



# Create your views here.



class InventoryView(viewsets.ModelViewSet) :
    queryset = Inventory.objects.all()
    serializer_class = InventoryWithSumSerializer
    permission_classes = (IsAuthenticatedCustom)



    def get_queryset(self):

        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        
        results = self.queryset.filter(**data)
        if keyword :
            search_fields = [
                "code", "created_by__fullname", "created_by__email","group__name", "name"
            ]
            query = get_query(keyword, search_fields)
            print(query)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        print(request.data)
        try :
            request.data._mutable = True
        except : 
            pass
        request.data.update({'created_by_id' : request.user.id})
        return super().create(request, *args, **kwargs)


class InventoryGroupView(viewsets.ModelViewSet) :
    queryset = InventoryGroup.objects.all()
    serializer_class = InventoryGroupSerializer
    permission_classes = (IsAuthenticatedCustom)




class ShopView(viewsets.ModelViewSet) :
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedCustom)


    def get_queryset(self):

        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        
        results = self.queryset.filter(**data)
        if keyword :
            search_fields = [
                "code", "created_by__fullname", "created_by__email","group__name", "name"
            ]
            query = get_query(keyword, search_fields)
            print(query)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data.update({'created_by_id' : request.user.id})
        return super().create(request, *args, **kwargs)


class InvoiceView(viewsets.ModelViewSet) :
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedCustom)

    def get_queryset(self):

        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        
        results = self.queryset.filter(**data)
        if keyword :
            search_fields = [
                "code", "created_by__fullname", "created_by__email","group__name", "name"
            ]
            query = get_query(keyword, search_fields)
            print(query)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        try :
            request.data._mutable = True
        except :pass
        request.data.update({"created_by_id":request.user.id})
        return super().create(request)



class InvoiceItemView(viewsets.ModelViewSet) :
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

    permission_classes = (IsAuthenticatedCustom)





class SalePerformanceView(viewsets.ModelViewSet) :
    http_method_names = ('get',)
    queryset = InventoryView.queryset
    serializer_class = InventoryView.serializer_class

    permission_classes = (IsAuthenticatedCustom)

    def list(self, request, *args, **kwargs):
        query_data = request.query_params.dict()
        total = query_data.get("total", None)
        query = self.queryset

        if not total :
            start_date = query_data.get("start_date", None)
            end_date = query_data.get('end_date', None)
            date = lambda item : datetime.strptime(item, "%d-%m-%Y")
            if start_date :
                query = query.filter(
                    created_at__range = [date(start_date), date(end_date)]
                )
        
        items = query.annotate(
            sum_of_item = Coalesce(
                Sum('inventory_invoices__quantity'), 0
            )
        ).order_by("-sum_of_item")[0:10]


        return Response(self.serializer_class(instance = items, many = True).data)


class SaleByShopView(viewsets.ModelViewSet) :
    http_method_names = ('get',)
    queryset = InventoryView.queryset
    permission_classes = (IsAuthenticatedCustom)


    def list(self, request, *args, **kwargs):

        data = request.query_params.dict()

        total = data.get("total", None)
        monthly = data.get("monthly")
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        date = lambda item : datetime.strptime(item, "%d-%m-%Y")

        query = ShopView.queryset


        if not total :
            query = query.filter(
                sale_shop__created_at__range = [date(start_date), date(end_date)]
            )

        if monthly :
            query = query.annotate(
                month = TruncMonth('created_at'),
            ).values("name", "month").annotate(amount_total = Sum(
                F("sale_shop__invoice_items__quantity") *
                F("sale_shop__invoice_items__amount")
            ))
        else :
            shops = query.annotate(amount_total=Sum(
                    F("sale_shop__invoice_items__quantity") * 
                    F("sale_shop__invoice_items__amount")
                )).order_by("-amount_total")


        response_data = ShopWithAmountSerializer(shops, many=True).data
        return Response(response_data)





class PurchaseView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    queryset = InvoiceView.queryset
    
    permission_classes = (IsAuthenticatedCustom)

    def list(self, request, *args, **kwargs):
        query_data = request.query_params.dict() 
        total = query_data.get('total', None)
        query = InvoiceItem.objects.select_related("invoice", "item")


        date = lambda item : datetime.strptime(item, "%d-%m-%Y")

        if not total:
            start_date = query_data.get("start_date", None)
            end_date = query_data.get("end_date", None)

            if start_date:
                query = query.filter(
                    created_at__range=[date(start_date), date(end_date)]
                )

        query = query.aggregate(
            amount_total=Sum(F('amount') * F('quantity')), total=Sum('quantity')
            )

        return Response({
            "price": "0.00" if not query.get("amount_total") else query.get("amount_total"),
            "count": 0 if not query.get("total") else query.get("total"),
        })
