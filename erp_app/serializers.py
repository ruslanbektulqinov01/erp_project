from django.utils import timezone
from rest_framework import serializers

from .models import (
    Archive,
    AttendanceRecord,
    BehaviorRecord,
    Branch,
    Customer,
    EduMetricSnapshot,
    GradeRecord,
    Order,
    PracticeRecord,
    Product,
    Region,
    Role,
    Staff,
    StudentProfile,
    User,
    Warehouse,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'


class DatedRecordValidationMixin:
    def validate_recorded_at(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("recorded_at future bo‘lishi mumkin emas.")
        return value


class GradeRecordSerializer(DatedRecordValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = GradeRecord
        fields = '__all__'


class AttendanceRecordSerializer(DatedRecordValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'


class BehaviorRecordSerializer(DatedRecordValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = BehaviorRecord
        fields = '__all__'


class PracticeRecordSerializer(DatedRecordValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = PracticeRecord
        fields = '__all__'


class EduMetricSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EduMetricSnapshot
        fields = '__all__'
