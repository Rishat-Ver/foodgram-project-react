from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from api.filters import NameSearchFilter
from api.pagination import CustumPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (FollowSerializer, IngredientSerializer,
                             MeUserSerializer, RecipeCreateSerializer,
                             RecipeReadSerializer, TagSerializer)
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
                return Response({"detail":'Нельзя подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(author=author, user=user).exists():
                return Response({"detail":'Вы уже подписаны!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author,
                                          context={"request": request})
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
    search_fields = ("^name",)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    '''Вюсет рецептов'''

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustumPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

