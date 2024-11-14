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

        def create(self, validated_data):
            return SubCategory.objects.create(**validated_data)


class MainCategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'order', 'sub_categories']

    def create(self, validated_data):
        sub_categories_data = validated_data.pop('sub_categories')
        main_category = MainCategory.objects.create(**validated_data)
        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(main_category=main_category, **sub_category_data)
        return main_category


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

    def create(self, validated_data):
        main_categories_data = validated_data.pop('main_categories')
        menu = Menu.objects.create(**validated_data)
        for main_category_data in main_categories_data:
            sub_categories_data = main_category_data.pop('sub_categories')
            main_category = MainCategory.objects.create(menu=menu, **main_category_data)
            for sub_category_data in sub_categories_data:
                SubCategory.objects.create(main_category=main_category, **sub_category_data)
        return menu

    def update(self, instance, validated_data):
        main_categories_data = validated_data.pop('main_categories', [])
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # main categories and sub-categories
        for main_category_data in main_categories_data:
            sub_categories_data = main_category_data.pop('sub_categories', [])
            main_category_id = main_category_data.get('id')

            if main_category_id:
                main_category = MainCategory.objects.get(id=main_category_id, menu=instance)
                main_category.name = main_category_data.get('name', main_category.name)
                main_category.order = main_category_data.get('order', main_category.order)
                main_category.save()
            else:
                main_category = MainCategory.objects.create(menu=instance, **main_category_data)

            for sub_category_data in sub_categories_data:
                sub_category_id = sub_category_data.get('id')
                if sub_category_id:
                    sub_category = SubCategory.objects.get(id=sub_category_id, main_category=main_category)
                    sub_category.name = sub_category_data.get('name', sub_category.name)
                    sub_category.order = sub_category_data.get('order', sub_category.order)
                    sub_category.photo = sub_category_data.get('photo', sub_category.photo)
                    sub_category.save()
                else:
                    SubCategory.objects.create(main_category=main_category, **sub_category_data)

        return instance
