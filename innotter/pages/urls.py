from rest_framework.routers import DefaultRouter

from .views import pages_view, PagesViewSet

router = DefaultRouter()
router.register(r'pages', PagesViewSet, basename='pages')
urlpatterns = router.urls
