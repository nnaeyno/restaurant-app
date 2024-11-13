from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, PublicRestaurantListView

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),

    path('public/restaurants/',
         PublicRestaurantListView.as_view(),
         name='public-restaurant-list'),
]