from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WorkPointViewSet, DailySummaryView, WorkPointReportView

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
        "workpoints/<uuid:id>/register-point/",
        WorkPointViewSet.as_view({"post": "register_point"}),
        name="register-point",
    ),
    path(
        "workpoints/<uuid:id>/register-point-manual/",
        WorkPointViewSet.as_view({"post": "register_point_manual"}),
        name="register-point-manual",
    ),
]
