from rest_framework.routers import DefaultRouter

from .views import posts_view, PostsViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
urlpatterns = router.urls
