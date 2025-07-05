from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.api_login, name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
