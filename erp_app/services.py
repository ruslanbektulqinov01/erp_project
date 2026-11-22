from dataclasses import dataclass

from django.db.models import Avg, F

from .models import EduMetricSnapshot, StudentProfile


@dataclass
class EduMetricResult:
    grade_index: float
    attendance_index: float
    behavior_index: float
    practice_index: float
    total_score: float
    trend: str
    risk_level: str


class EduMetricCalculator:
    WEIGHTS = {
        "grade": 0.45,
        "attendance": 0.20,
        "behavior": 0.15,
        "practice": 0.20,
    }

    @classmethod
    def calculate(cls, student: StudentProfile) -> EduMetricResult:
        grade_index = student.grades.aggregate(v=Avg(100 * F("score") / F("max_score")))["v"] or 0

        attendance_total = student.attendance.count()
        attendance_effective = student.attendance.exclude(state="absent", is_excused=False).count()
        attendance_index = (attendance_effective / attendance_total) * 100 if attendance_total else 0

        behavior_raw = student.behavior.aggregate(d=Avg("discipline"), t=Avg("teamwork"), l=Avg("leadership"))
        behavior_index = ((behavior_raw["d"] or 0) + (behavior_raw["t"] or 0) + (behavior_raw["l"] or 0)) / 3 * 10

        practice_index = student.practice.aggregate(v=Avg("final_score"))["v"] or 0

        total_score = (
            (grade_index * cls.WEIGHTS["grade"])
            + (attendance_index * cls.WEIGHTS["attendance"])
            + (behavior_index * cls.WEIGHTS["behavior"])
            + (practice_index * cls.WEIGHTS["practice"])
        )

        snapshots = student.snapshots.order_by("-created_at")[:4]
        prev_score = snapshots[0].total_score if snapshots else None
        trend = "stable"
        if prev_score is not None and total_score > prev_score + 2:
            trend = "improving"
        elif prev_score is not None and total_score < prev_score - 2:
            trend = "declining"

        risk = "low"
        if attendance_index < 70 or total_score < 60:
            risk = "high"
        elif total_score < 75:
            risk = "medium"

        return EduMetricResult(
            grade_index=round(grade_index, 2),
            attendance_index=round(attendance_index, 2),
            behavior_index=round(behavior_index, 2),
            practice_index=round(practice_index, 2),
            total_score=round(total_score, 2),
            trend=trend,
            risk_level=risk,
        )


class EduMetricSnapshotService:
    @staticmethod
    def create_snapshot(student: StudentProfile) -> EduMetricSnapshot:
        result = EduMetricCalculator.calculate(student)
        return EduMetricSnapshot.objects.create(student=student, **result.__dict__)
