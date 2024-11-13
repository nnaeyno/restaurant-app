from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meal.views import DishViewSet, PublicDishListView

router = DefaultRouter()

router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('', include(router.urls)),
    path('public/dishes/',
         PublicDishListView.as_view(),
         name='public-dish-list'),
]