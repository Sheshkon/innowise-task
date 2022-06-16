from rest_framework.routers import DefaultRouter

from .views import PagesBaseViewSet, TagsBaseViewSet, PostsBaseViewSet

router = DefaultRouter()

router.register(r'pages', PagesBaseViewSet, basename='pages')
router.register(r'tags', TagsBaseViewSet, basename='tags')
router.register(r'posts', PostsBaseViewSet, basename='posts')

urlpatterns = router.urls
