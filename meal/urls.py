from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meal.views import DishViewSet, PublicDishListView, DishAPIView

router = DefaultRouter()

router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('', include(router.urls)),
    path('public/dishes/',
         PublicDishListView.as_view(),
         name='public-dish-list'),
    path('dish-create/', DishAPIView.as_view(), name='dish-create'),
    path('dishes/<int:pk>/', DishAPIView.as_view(), name='dish-update'),
]