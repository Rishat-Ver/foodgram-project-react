from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustumUserViewSet, IngredientViewSet,
                       TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('users', CustumUserViewSet)
# router.register(r'users/(?P<user_id>\d+)/', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
