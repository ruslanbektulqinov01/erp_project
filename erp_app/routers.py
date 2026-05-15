from rest_framework import routers
from .views import (
    DirectorViewSet,
    Manager1ViewSet,
    Manager2ViewSet,
    Manager3ViewSet,
    AccountantViewSet,
    SellerViewSet,
    StudentProfileViewSet,
    GradeRecordViewSet,
    AttendanceRecordViewSet,
    BehaviorRecordViewSet,
    PracticeRecordViewSet,
)

router = routers.DefaultRouter()
router.register(r'directors', DirectorViewSet, basename='director')
router.register(r'managers1', Manager1ViewSet, basename='manager1')
router.register(r'managers2', Manager2ViewSet, basename='manager2')
router.register(r'managers3', Manager3ViewSet, basename='manager3')
router.register(r'accountants', AccountantViewSet, basename='accountant')
router.register(r'sellers', SellerViewSet, basename='seller')

# EduMetric endpoints
router.register(r'students', StudentProfileViewSet, basename='students')
router.register(r'grades', GradeRecordViewSet, basename='grades')
router.register(r'attendance', AttendanceRecordViewSet, basename='attendance')
router.register(r'behavior', BehaviorRecordViewSet, basename='behavior')
router.register(r'practice', PracticeRecordViewSet, basename='practice')

urlpatterns = router.urls
