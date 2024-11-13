from rest_framework import serializers

from meal.serializers import DishSerializer, PublicDishSerializer
from .models import Menu, MainCategory, SubCategory
from restaurant.models import Restaurant


class PublicMainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ['id', 'name']


class PublicSubCategorySerializer(serializers.ModelSerializer):
    dishes = PublicDishSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'photo', 'dishes']


class SubCategorySerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'photo', 'order', 'dishes']


class MainCategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'order', 'sub_categories']


class MenuSerializer(serializers.ModelSerializer):
    main_categories = MainCategorySerializer(many=True, read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all()
    )

    class Meta:
        model = Menu
        fields = ['id', 'name', 'restaurant', 'is_active', 'main_categories']

    def validate_restaurant(self, value):
        user = self.context['request'].user
        if not user.is_staff and value.owner != user:
            raise serializers.ValidationError(
                "You can only create menus for your own restaurants."
            )
        return value
