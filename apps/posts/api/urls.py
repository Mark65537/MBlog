from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from .views import LikeViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = router.urls