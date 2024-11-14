from rest_framework import serializers
from .models import Dish, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'is_allergen']


class PublicDishListSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ['id', 'name', 'photo', 'ingredients', 'price', 'is_available']

    def get_ingredients(self, obj):
        dish_ingredients = obj.dish_ingredients.select_related('ingredient')
        return [
            {
                'name': di.ingredient.name,
                'is_allergen': di.ingredient.is_allergen,
                'is_optional': di.is_optional
            }
            for di in dish_ingredients
        ]


class PublicDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'photo', 'is_available']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'sub_category', 'name', 'description', 'price', 'photo',
                  'is_available', 'order']
