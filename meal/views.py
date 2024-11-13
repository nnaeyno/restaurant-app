from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from meal.filters import DishFilter
from meal.models import Dish
from meal.serializers import DishSerializer, PublicDishListSerializer
from restaurant.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PublicDishListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicDishListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DishFilter
    search_fields = ['name', 'ingredients__name']
    ordering_fields = ['name', 'price']
    ordering = ['name']

    def get_queryset(self):
        return Dish.objects.select_related(
            'sub_category'
        ).prefetch_related(
            'dish_ingredients__ingredient'
        ).filter(
            sub_category__main_category__menu__is_active=True,
            sub_category__main_category__menu__restaurant__is_active=True
        ).distinct()


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Dish.objects.all()
        return Dish.objects.filter(
            sub_category__main_category__menu__restaurant__owner=self.request.user
        )
