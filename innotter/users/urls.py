from rest_framework.routers import DefaultRouter

from .views import users_view, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = router.urls
