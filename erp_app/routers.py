from rest_framework import routers
from .views import DirectorViewSet, Manager1ViewSet, Manager2ViewSet, Manager3ViewSet, AccountantViewSet, SellerViewSet

router = routers.DefaultRouter()
router.register(r'directors', DirectorViewSet, basename='director')
router.register(r'managers1', Manager1ViewSet, basename='manager1')
router.register(r'managers2', Manager2ViewSet, basename='manager2')
router.register(r'managers3', Manager3ViewSet, basename='manager3')
router.register(r'accountants', AccountantViewSet, basename='accountant')
router.register(r'sellers', SellerViewSet, basename='seller')

urlpatterns = router.urls
