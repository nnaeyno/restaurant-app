from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, SubCategoryViewSet, PublicMainCategoryView, PublicSubCategoryView, MenuAPIView

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')

urlpatterns = [
    path('', include(router.urls)),

    path('public/main-categories/',
         PublicMainCategoryView.as_view(),
         name='public-main-categories'),

    path('public/sub-categories/',
         PublicSubCategoryView.as_view(),
         name='public-sub-categories'),

    path('menu/', MenuAPIView.as_view(), name='menu-create'),
    path('menu/<int:pk>/', MenuAPIView.as_view(), name='menu-update'),
]