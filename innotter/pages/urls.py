from rest_framework.routers import DefaultRouter

from .views import PagesViewSet, TagsViewSet, PostsViewSet, LikeViewSet

router = DefaultRouter()

router.register(r'pages', PagesViewSet, basename='pages')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'likes', LikeViewSet, basename='likes')

urlpatterns = router.urls
