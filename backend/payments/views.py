
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Business, PaymentOrder, PaymentTransaction, AuditLog
from .serializers import (
    BusinessSerializer,
    PaymentOrderSerializer,
    PaymentTransactionSerializer,
    AuditLogSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response(
        {
            "system": "Sholix Payment System",
            "short_name": "SPS",
            "status": "healthy",
            "message": "SPS backend is running successfully.",
        },
        status=status.HTTP_200_OK,
    )


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all().order_by("-created_at")
    serializer_class = BusinessSerializer
    permission_classes = [IsAdminUser]


class PaymentOrderViewSet(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.select_related("business").all()
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAdminUser]


class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentTransaction.objects.select_related(
        "order", "order__business"
    ).all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAdminUser]


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("business", "actor").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]

from django.db.models import Sum, Q
from rest_framework.views import APIView


class DashboardSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = PaymentOrder.objects.all()

        successful_collections = orders.filter(
            direction=PaymentOrder.Direction.COLLECTION,
            status=PaymentOrder.Status.SUCCESSFUL,
        ).aggregate(total=Sum("amount"))["total"]

        recent_orders = orders.select_related("business").order_by(
            "-created_at"
        )[:10]

        return Response({
            "system": "Sholix Payment System",
            "currency": "KES",
            "businesses_count": Business.objects.count(),
            "payment_orders_count": orders.count(),
            "pending_orders_count": orders.filter(
                status=PaymentOrder.Status.PENDING
            ).count(),
            "processing_orders_count": orders.filter(
                status=PaymentOrder.Status.PROCESSING
            ).count(),
            "successful_orders_count": orders.filter(
                status=PaymentOrder.Status.SUCCESSFUL
            ).count(),
            "failed_orders_count": orders.filter(
                status=PaymentOrder.Status.FAILED
            ).count(),
            "successful_collection_orders_total": str(
                successful_collections or 0
            ),
            "recent_orders": PaymentOrderSerializer(
                recent_orders, many=True
            ).data,
        })
