from rest_framework.routers import DefaultRouter

from .views import tags_view, TagsViewSet


router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
urlpatterns = router.urls
