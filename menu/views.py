from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from rest_framework.views import APIView

from .models import Menu, SubCategory, MainCategory
from .serializers import (
    MenuSerializer, MainCategorySerializer,
    SubCategorySerializer, PublicSubCategorySerializer, PublicMainCategorySerializer
)
from restaurant.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as django_filters
from rest_framework.response import Response


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Menu.objects.all()
        return Menu.objects.filter(restaurant__owner=self.request.user)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def add_main_category(self, request, pk=None):
        menu = self.get_object()
        serializer = MainCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(menu=menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        if self.request.user.is_staff:
            return SubCategory.objects.all()
        return SubCategory.objects.filter(
            main_category__menu__restaurant__owner=self.request.user
        )


class MainCategoryFilter(django_filters.FilterSet):
    menu_id = django_filters.NumberFilter(field_name='menu__id')

    class Meta:
        model = MainCategory
        fields = ['menu_id']


class PublicMainCategoryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicMainCategorySerializer
    queryset = MainCategory.objects.all()
    filterset_class = MainCategoryFilter


class SubCategoryFilter(django_filters.FilterSet):
    main_category = django_filters.NumberFilter(field_name='main_category__id')
    dish_name = django_filters.CharFilter(
        field_name='dishes__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = SubCategory
        fields = ['main_category', 'dish_name']


class PublicSubCategoryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicSubCategorySerializer
    queryset = SubCategory.objects.all()
    filterset_class = SubCategoryFilter
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['dishes__name']

    def get_queryset(self):
        queryset = SubCategory.objects.prefetch_related(
            'dishes'
        ).filter(
            main_category__menu__is_active=True,
            main_category__menu__restaurant__is_active=True
        )

        # Filter by dish availability if requested
        show_available = self.request.query_params.get('available_only', 'false').lower() == 'true'
        if show_available:
            queryset = queryset.filter(dishes__is_available=True)

        return queryset.distinct()


class MenuAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MenuSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(menu, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)