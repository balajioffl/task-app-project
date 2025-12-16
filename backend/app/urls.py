from django.urls import path
from .views import check, test_api
from rest_framework_simplejwt.views import(TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path("check/", check, name="check"),
    path("login/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_api, name='test_api'),
]