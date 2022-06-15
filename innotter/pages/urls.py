from rest_framework.routers import DefaultRouter

from .views import pages_view, PagesViewSet, TagsViewSet, PostsViewSet

router = DefaultRouter()

router.register(r'pages', PagesViewSet, basename='pages')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'posts', PostsViewSet, basename='posts')

urlpatterns = router.urls
