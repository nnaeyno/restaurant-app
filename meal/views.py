from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class DishAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DishSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            dish = Dish.objects.get(pk=pk)
        except Dish.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DishSerializer(dish, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)