from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Archive,
    AttendanceRecord,
    BehaviorRecord,
    Branch,
    GradeRecord,
    Order,
    PracticeRecord,
    Product,
    Staff,
    StudentProfile,
)
from .serializers import (
    ArchiveSerializer,
    AttendanceRecordSerializer,
    BehaviorRecordSerializer,
    BranchSerializer,
    EduMetricSnapshotSerializer,
    GradeRecordSerializer,
    OrderSerializer,
    PracticeRecordSerializer,
    ProductSerializer,
    StaffSerializer,
    StudentProfileSerializer,
)
from .services import EduMetricSnapshotService


class DirectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    def list(self, request, *args, **kwargs):
        daily_revenue = self.queryset.filter(order__create_at__date=timezone.now().date()).aggregate(revenue=Sum('revenue'))['revenue']
        monthly_revenue = self.queryset.filter(order__create_at__month=timezone.now().month).aggregate(revenue=Sum('revenue'))['revenue']
        annual_revenue = self.queryset.filter(order__create_at__year=timezone.now().year).aggregate(revenue=Sum('revenue'))['revenue']
        return Response({'daily_revenue': daily_revenue, 'monthly_revenue': monthly_revenue, 'annual_revenue': annual_revenue})


class Manager1ViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class Manager2ViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user').all().order_by('-id')
    serializer_class = StudentProfileSerializer

    def get_queryset(self):
        queryset = self.queryset
        faculty = self.request.query_params.get('faculty')
        group_name = self.request.query_params.get('group_name')
        status_value = self.request.query_params.get('status')

        if faculty:
            queryset = queryset.filter(faculty__icontains=faculty)
        if group_name:
            queryset = queryset.filter(group_name__icontains=group_name)
        if status_value:
            queryset = queryset.filter(status=status_value)
        return queryset

    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        student = self.get_object()
        snapshot = EduMetricSnapshotService.create_snapshot(student)
        return Response(EduMetricSnapshotSerializer(snapshot).data)


class GradeRecordViewSet(viewsets.ModelViewSet):
    queryset = GradeRecord.objects.select_related('student').all().order_by('-recorded_at', '-id')
    serializer_class = GradeRecordSerializer

    def get_queryset(self):
        queryset = self.queryset
        student_id = self.request.query_params.get('student')
        subject = self.request.query_params.get('subject')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        return queryset


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('student').all().order_by('-recorded_at', '-id')
    serializer_class = AttendanceRecordSerializer

    def get_queryset(self):
        queryset = self.queryset
        student_id = self.request.query_params.get('student')
        state = self.request.query_params.get('state')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if state:
            queryset = queryset.filter(state=state)
        return queryset


class BehaviorRecordViewSet(viewsets.ModelViewSet):
    queryset = BehaviorRecord.objects.select_related('student').all().order_by('-recorded_at', '-id')
    serializer_class = BehaviorRecordSerializer

    def get_queryset(self):
        queryset = self.queryset
        student_id = self.request.query_params.get('student')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset


class PracticeRecordViewSet(viewsets.ModelViewSet):
    queryset = PracticeRecord.objects.select_related('student').all().order_by('-recorded_at', '-id')
    serializer_class = PracticeRecordSerializer

    def get_queryset(self):
        queryset = self.queryset
        student_id = self.request.query_params.get('student')
        company = self.request.query_params.get('company')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if company:
            queryset = queryset.filter(company__icontains=company)
        return queryset


def edumetric_dashboard(request):
    return render(request, "edumetric/dashboard.html")
