from rest_framework import serializers
from .models import Restaurant, Address


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code', 'country']


class RestaurantSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'phone_number', 'photo', 'address', 'owner', 'is_active']
        read_only_fields = ['id', 'is_active']

    def validate_photo(self, value):
        # TO DO add photo size validation

        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG and PNG files are allowed")

        return value

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        restaurant = Restaurant.objects.create(**validated_data)
        Address.objects.create(restaurant=restaurant, **address_data)
        return restaurant

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        return instance
