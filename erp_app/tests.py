from datetime import date

from django.test import TestCase

from .models import (
    AttendanceRecord,
    BehaviorRecord,
    GradeRecord,
    PracticeRecord,
    Role,
    StudentProfile,
    User,
)
from .services import EduMetricCalculator


class EduMetricCalculatorTests(TestCase):
    def setUp(self):
        role = Role.objects.create(name="student", description="student role")
        user = User.objects.create_user(username="std1", password="pass12345", role=role)
        self.student = StudentProfile.objects.create(
            user=user,
            student_id="STU-0001",
            faculty="Engineering",
            program="SE",
            group_name="SE-24-01",
            course=2,
        )

    def test_calculate_metrics_and_risk(self):
        GradeRecord.objects.create(student=self.student, subject="Math", score=80, max_score=100, recorded_at=date.today())
        AttendanceRecord.objects.create(student=self.student, subject="Math", state="present", recorded_at=date.today())
        AttendanceRecord.objects.create(student=self.student, subject="Physics", state="absent", is_excused=False, recorded_at=date.today())
        BehaviorRecord.objects.create(student=self.student, discipline=8, teamwork=7, leadership=9, recorded_at=date.today())
        PracticeRecord.objects.create(student=self.student, company="Acme", kpi_score=78, final_score=82, recorded_at=date.today())

        result = EduMetricCalculator.calculate(self.student)

        self.assertGreaterEqual(result.total_score, 0)
        self.assertLessEqual(result.total_score, 100)
        self.assertIn(result.risk_level, ["low", "medium", "high"])
        self.assertIn(result.trend, ["stable", "improving", "declining"])

    def test_low_attendance_forces_high_risk(self):
        GradeRecord.objects.create(student=self.student, subject="Math", score=95, max_score=100, recorded_at=date.today())
        AttendanceRecord.objects.create(student=self.student, subject="Math", state="absent", is_excused=False, recorded_at=date.today())
        result = EduMetricCalculator.calculate(self.student)
        self.assertEqual(result.risk_level, "high")
