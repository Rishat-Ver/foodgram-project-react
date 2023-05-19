from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingCart, Tag)
from users.models import Follow, User

from django.shortcuts import get_object_or_404




class MeUserSerializer(UserSerializer):
    '''Пользовательский сериализатор.'''

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class FollowSerializer(MeUserSerializer):
    '''Сериализатор подписoк.'''

    recipes_count = serializers.IntegerField(source='recipes.count',    
                                             read_only = True)
    recipes = SerializerMethodField(method_name='get_recipes')
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'recipes_count', 'recipes',
                  'is_subscribed')
        read_only_fields = ('email', 'username',
                            'first_name', 'last_name')

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        serializer = RecipeShortSerializer(recipes, many=True,
                                           context=self.context)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор тегов.'''

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор ингридиентов.'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeShortSerializer(ModelSerializer):
    '''Сериализатор для отображения рецептов на странице подписок.'''

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientInRecipeCreateSerializer(ModelSerializer):
    '''Сериализатор для отоброжения ингридиента при создание рецепта'''

    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeReadSerializer(ModelSerializer):
    '''Сериализатор получения рецепта.'''

    tags = TagSerializer(many=True, read_only=True)
    author = MeUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favourite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeCreateSerializer(ModelSerializer):
    '''Сериализатор создания рецепта'''

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    author = MeUserSerializer(read_only=True)
    ingredients = IngredientInRecipeCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(), fields=('ingredients'))]

    def validate_tags(self, value):
        if not value:
            raise ValidationError('Нужно добавить тег.')
        return value

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError('Нужно добавить ингридиент.')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            RecipeIngredients.objects.create(recipe=recipe,
                                             ingredient=ingredient,
                                             amount=amount)
        for tag in tags:
            Tag.objects.create(recipe=recipe, tag=tag)
        return recipe
