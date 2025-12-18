from django.urls import path,include
from .views import check, test_api,get_user_role
from rest_framework_simplejwt.views import(TokenObtainPairView,TokenRefreshView)

from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path("check/", check, name="check"),
    path("login/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_api, name='test_api'),
    path("user-role/", get_user_role),
    path("", include(router.urls)),
]



