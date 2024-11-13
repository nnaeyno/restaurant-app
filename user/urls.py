from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='login'),
]
