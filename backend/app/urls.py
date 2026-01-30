from django.urls import path, include
from .views import check, test_api, get_user_groups, profile, user_list
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    export_csv,
    export_pdf,
    ProfileView,
    ProfileUpdate,
    ProfileDelete,
    # task_debug_view
)

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("check/", check, name="check"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("test/", test_api, name="test_api"),
    path("user-groups/", get_user_groups),
    path("users/", user_list, name="view-list"),
    path("export/tasks/csv/", export_csv),
    path("export/tasks/pdf/", export_pdf),
    path("profile/", ProfileView.as_view()),
    path("profile/bio-pic/", ProfileUpdate.as_view()),
    path("profile/bio-pic/delete/", ProfileDelete.as_view()),
    # path("debug/tasks/", task_debug_view),
    path("", include(router.urls)),
]
