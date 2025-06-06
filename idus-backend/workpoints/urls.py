from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    WorkPointViewSet,
    DailySummaryView,
    WorkPointReportView,
    WorkPointPDFReportView,
    UserWorkPointView,
)


router = DefaultRouter()
router.register(r"workpoints", WorkPointViewSet, basename="workpoint")

urlpatterns = [
    path("", include(router.urls)),
    path("summary/", DailySummaryView.as_view(), name="workpoint-summary"),
    path("summary/<uuid:id>/", DailySummaryView.as_view(), name="workpoint-summary-id"),
    path(
        "workpoints/report/<uuid:id>/",
        WorkPointReportView.as_view(),
        name="workpoint-report-id",
    ),
    path("workpoints/report/", WorkPointReportView.as_view(), name="workpoint-report"),
    path(
        "users/<uuid:user_id>/workpoints/register-point/",
        UserWorkPointView.as_view({"post": "register_point"}),
        name="register-point",
    ),
    path(
        "users/<uuid:user_id>/workpoints/register-point-manual/",
        UserWorkPointView.as_view({"post": "register_point_manual"}),
        name="register-point-manual",
    ),
    path(
        "workpoints/report/<uuid:id>/pdf/",
        WorkPointPDFReportView.as_view(),
        name="workpoint-report-pdf",
    ),
]
