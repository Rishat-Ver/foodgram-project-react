from djoser.serializers import UserSerializer
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from rest_framework.fields import ImageField, SerializerMethodField
from rest_framework.serializers import ModelSerializer


from users.models import Follow, User


class CustumUserSerializer(UserSerializer):
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


class FollowSerializer(CustumUserSerializer):
    recipes_count = SerializerMethodField()
    # recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes_count',
                  'recipes')
        read_only_fields = ('email', 'username')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self):
        pass


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustumUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return obj.is_favorited(request.user)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return obj.is_in_shopping_cart(request.user)