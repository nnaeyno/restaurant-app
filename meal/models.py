from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db import models
from menu.models import SubCategory


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    is_allergen = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        'Dish',
        on_delete=models.CASCADE,
        related_name='dish_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='dish_ingredients'
    )
    is_optional = models.BooleanField(default=False)

    class Meta:
        unique_together = ['dish', 'ingredient']


class Dish(models.Model):
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='dishes'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    photo = models.ImageField(upload_to='menus/dishes/%Y/%m/%d/')
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishIngredient',
        related_name='dishes'
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Dishes'
