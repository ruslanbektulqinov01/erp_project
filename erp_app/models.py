from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True)

    groups = models.ManyToManyField(Group, blank=True, related_name="erp_app_users")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="erp_app_users")


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    salary = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    map = models.TextField()

    def __str__(self):
        return self.first_name


class Product(models.Model):
    STATUS_CHOICE = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    CATEGORY_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('children', 'Children'),
    )
    name = models.CharField(max_length=255)
    brend = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    description = models.TextField()
    unit_cost = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    count = models.IntegerField()
    color = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    status = models.CharField(max_length=255, choices=STATUS_CHOICE, default='PENDING')

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    product_count = models.IntegerField()

    def __str__(self):
        return self.location


class Order(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('online', 'Online'),
    )
    cost_price = models.DecimalField(max_digits=5, decimal_places=2)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_count = models.IntegerField()
    payment = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    sold = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Archive(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    revenue = models.IntegerField()

    def __str__(self):
        return f'{self.customer.first_name}'


# EduMetric domain models
class StudentProfile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        GRADUATED = "graduated", "Graduated"
        DROPPED = "dropped", "Dropped"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=32, unique=True)
    faculty = models.CharField(max_length=120)
    program = models.CharField(max_length=120)
    group_name = models.CharField(max_length=80)
    course = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)


class GradeRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grades")
    subject = models.CharField(max_length=120)
    score = models.FloatField()
    max_score = models.FloatField(default=100)
    recorded_at = models.DateField()


class AttendanceRecord(models.Model):
    class AttendanceState(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LATE = "late", "Late"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendance")
    subject = models.CharField(max_length=120)
    state = models.CharField(max_length=12, choices=AttendanceState.choices)
    is_excused = models.BooleanField(default=False)
    recorded_at = models.DateField()


class BehaviorRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="behavior")
    discipline = models.PositiveSmallIntegerField()
    teamwork = models.PositiveSmallIntegerField()
    leadership = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    recorded_at = models.DateField()


class PracticeRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="practice")
    company = models.CharField(max_length=120)
    kpi_score = models.FloatField()
    final_score = models.FloatField()
    recorded_at = models.DateField()


class EduMetricSnapshot(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="snapshots")
    grade_index = models.FloatField()
    attendance_index = models.FloatField()
    behavior_index = models.FloatField()
    practice_index = models.FloatField()
    total_score = models.FloatField()
    trend = models.CharField(max_length=16)
    risk_level = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
