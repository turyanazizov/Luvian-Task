from rest_framework import routers
from main.viewsets import ProductViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('register', UserViewSet)
router.register('products', ProductViewSet)
