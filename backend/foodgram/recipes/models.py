from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from api.validators import validate_year
from users.models import User


class Tag(models.Model):
    '''Модель тегов'''

    name = models.CharField(verbose_name='Имя тега',
                            max_length=200,
                            unique=True)
    color = models.CharField(verbose_name='Цвет',
                             max_length=7,
                             unique=True)
    slug = models.SlugField(verbose_name='Слаг',
                            max_length=200,
                            unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Модель Ингридиент'''

    name = models.CharField(verbose_name='Название',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=200)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['pk',]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Модель Рецепт'''

    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='recipes',)
    name = models.CharField(verbose_name='Название',
                            max_length=200)
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='recipes/')
    text = models.TextField(verbose_name='Текст')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингридиенты',
                                         through='RecipeIngredients',
                                         related_name='recipes')

    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тег',
                                  related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')
    date = models.DateTimeField(verbose_name='Дата публикации',
                                validators=(validate_year,),
                                auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date',)

    def __str__(self):
        return str(self.name)


class RecipeIngredients(models.Model):
    '''Модель ингридиенты для рецепта'''

    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='recipeingredients')
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Ингридиент',
                                   on_delete=models.CASCADE,
                                   related_name='recipeingredients')
    amount = models.PositiveSmallIntegerField(verbose_name='Колличество',
                                              validators=(MinValueValidator(1),))

    class Meta:
        verbose_name = 'ингридиент для рецепта'
        verbose_name_plural = 'ингридиенты для рецепта'

    def __str__(self):
        return f'{str(self.ingredient)} in {str(self.recipe)}-{self.amount}'


class Favourite(models.Model):
    '''Модель Избранное'''

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favourite')
        ]

    def __str__(self):
        return f'Добавленно в избранное {self.recipe}'


class ShoppingCart(models.Model):
    '''Модель Список покупок'''

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='shopping')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='shopping')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Список Покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'Добавил в корзину {self.recipe}'
