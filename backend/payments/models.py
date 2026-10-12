
from django.conf import settings
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    currency = models.CharField(max_length=3, default="KES")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PaymentOrder(models.Model):
    class Direction(models.TextChoices):
        COLLECTION = "collection", "Collection"
        PAYOUT = "payout", "Payout"

    class Channel(models.TextChoices):
        MPESA = "mpesa", "M-Pesa"
        BANK = "bank", "Bank"
        CARD = "card", "Card"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SUCCESSFUL = "successful", "Successful"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name="payment_orders",
    )
    reference = models.CharField(max_length=100, unique=True)
    direction = models.CharField(
        max_length=20,
        choices=Direction.choices,
        default=Direction.COLLECTION,
    )
    channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        default=Channel.MPESA,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="KES")
    customer_name = models.CharField(max_length=200, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=250, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    idempotency_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.amount} {self.currency}"


class PaymentTransaction(models.Model):
    order = models.ForeignKey(
        PaymentOrder,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    provider = models.CharField(max_length=50, default="manual")
    provider_reference = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentOrder.Status.choices,
        default=PaymentOrder.Status.PENDING,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="KES")
    provider_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.reference} - {self.status}"


class AuditLog(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.created_at}"


class MpesaPayment(models.Model):
    class Method(models.TextChoices):
        STK_PUSH = "stk_push", "STK Push"
        C2B = "c2b", "Paybill/Till (C2B)"

    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        FAILED = "failed", "Failed"
        REVIEW = "review", "Needs Review"

    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name="mpesa_payments",
        null=True,
        blank=True,
    )
    matched_order = models.ForeignKey(
        PaymentOrder,
        on_delete=models.SET_NULL,
        related_name="mpesa_payments",
        null=True,
        blank=True,
    )
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
    )
    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )
    checkout_request_id = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    merchant_request_id = models.CharField(
        max_length=150,
        blank=True,
    )
    business_shortcode = models.CharField(max_length=30, blank=True)
    account_reference = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="KES")
    transaction_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REVIEW,
    )
    result_code = models.CharField(max_length=20, blank=True)
    result_description = models.TextField(blank=True)
    provider_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"M-Pesa {self.receipt_number or self.checkout_request_id}"
        )
