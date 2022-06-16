from rest_framework.routers import DefaultRouter

from .views import UserBaseViewSet

router = DefaultRouter()
router.register(r'users', UserBaseViewSet, basename='users')
urlpatterns = router.urls
