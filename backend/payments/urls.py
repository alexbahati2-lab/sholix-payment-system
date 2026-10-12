from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    health_check,
    BusinessViewSet,
    PaymentOrderViewSet,
    PaymentTransactionViewSet,
    AuditLogViewSet,
    DashboardSummaryView,
)

router = DefaultRouter()
router.register("businesses", BusinessViewSet, basename="business")
router.register("payment-orders", PaymentOrderViewSet, basename="payment-order")
router.register(
    "transactions",
    PaymentTransactionViewSet,
    basename="transaction",
)
router.register("audit-logs", AuditLogViewSet, basename="audit-log")

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("dashboard/", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("", include(router.urls)),
]