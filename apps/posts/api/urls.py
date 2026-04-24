from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from .views import LikeViewSet
from .views import CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls