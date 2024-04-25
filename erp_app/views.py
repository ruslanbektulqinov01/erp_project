from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta


class DirectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    def list(self, request, *args, **kwargs):
        daily_revenue = \
            self.queryset.filter(order__create_at__date=timezone.now().date()).aggregate(revenue=Sum('revenue'))[
                'revenue']
        monthly_revenue = \
            self.queryset.filter(order__create_at__month=timezone.now().month).aggregate(revenue=Sum('revenue'))[
                'revenue']
        annual_revenue = \
            self.queryset.filter(order__create_at__year=timezone.now().year).aggregate(revenue=Sum('revenue'))[
                'revenue']
        return Response({
            'daily_revenue': daily_revenue,
            'monthly_revenue': monthly_revenue,
            'annual_revenue': annual_revenue,
        })


class Manager1ViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if self.queryset.filter(name=name).exists():
            return Response({'error': 'Product with this name already exists.'}, status=400)
        return super().create(request, *args, **kwargs)


class Manager2ViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def partial_update(self, request, *args, **kwargs):
        if 'product_status' not in request.data:
            return Response({'error': 'Only product status can be updated.'}, status=400)
        return super().partial_update(request, *args, **kwargs)


class Manager3ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def list(self, request, *args, **kwargs):
        branches = self.queryset.annotate(product_count=Count('warehouse__product'))
        serializer = self.get_serializer(branches, many=True)
        return Response(serializer.data)


class AccountantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        branch_id = request.data.get('branch')
        product_count = request.data.get('product_count')
        product = Product.objects.get(id=product_id)
        branch = Branch.objects.get(id=branch_id)
        if branch.warehouse.product != product or branch.warehouse.count < product_count:
            return Response({'error': 'Not enough product in the warehouse.'}, status=400)
        branch.warehouse.count -= product_count
        branch.warehouse.save()
        return super().create(request, *args, **kwargs)
