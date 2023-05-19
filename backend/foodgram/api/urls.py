from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, MeUserViewSet, RecipeViewSet,
                       TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', MeUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
