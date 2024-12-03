from django.urls import path
from .views import (
    UserCreateView,
    UserInfoView,
    UserListView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("info/", UserInfoView.as_view(), name="user-info"),
    path("info/<uuid:id>/", UserInfoView.as_view(), name="user-info-id"),
    path("list/", UserListView.as_view(), name="user-list"),
    path("update/<uuid:id>/", UserUpdateView.as_view(), name="user-update"),
    path("delete/<uuid:id>/", UserDeleteView.as_view(), name="user-delete"),
]
