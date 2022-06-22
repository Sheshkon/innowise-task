from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = router.urls
# urlpatterns += path('login/', login_view)

# urlpatterns = [
#     path('login/', login_view, name='login')
# ]
