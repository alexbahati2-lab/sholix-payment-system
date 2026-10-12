
from django.contrib import admin
from .models import Business, PaymentOrder, PaymentTransaction, AuditLog


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "currency", "is_active")
    search_fields = ("name", "legal_name", "phone", "email")
    list_filter = ("is_active", "currency")


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "business",
        "direction",
        "channel",
        "amount",
        "currency",
        "status",
        "created_at",
    )
    search_fields = (
        "reference",
        "customer_name",
        "customer_phone",
    )
    list_filter = ("direction", "channel", "status", "currency")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "provider",
        "provider_reference",
        "status",
        "amount",
        "currency",
        "created_at",
    )
    search_fields = ("provider_reference", "order__reference")
    list_filter = ("provider", "status", "currency")
    readonly_fields = ("created_at",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "actor", "action", "created_at")
    search_fields = ("action",)
    list_filter = ("action", "created_at")
    readonly_fields = ("created_at",)
