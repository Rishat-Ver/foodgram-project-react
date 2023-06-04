from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from api.filters import NameSearchFilter, RecipeFilter
from api.pagination import CustumPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (FollowSerializer, IngredientSerializer,
                             MeUserSerializer, RecipeCreateSerializer,
                             RecipeReadSerializer, RecipeShortSerializer,
                             TagSerializer)
from api.utils import download_cart
from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingCart, Tag)
from users.models import Follow, User


class MeUserViewSet(UserViewSet):
    '''Вьюсет для пользователей и подписок'''

    queryset = User.objects.all()
    serializer_class = MeUserSerializer
    pagination_class = CustumPagination

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user.id == author.id:
                return Response({'detail': 'Нельзя подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(author=author, user=user).exists():
                return Response({'detail': 'Вы уже подписаны!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author,
                                          context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response({'errors': 'Вы не подписаны'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscription = get_object_or_404(Follow,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет тегов'''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет ингридиентов'''

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (NameSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    '''Вюсет рецептов'''

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustumPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']
    ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if Favourite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favourite.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(
                recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Favourite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепта нет в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            favorite = get_object_or_404(Favourite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Уже в списке'},
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(
                recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not ShoppingCart.objects.filter(user=user,
                                               recipe=recipe).exists():
                return Response({'errors': 'Рецепта нет в списке покупок'},
                                status=status.HTTP_400_BAD_REQUEST)
            shopping_cart = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        return download_cart(request)
