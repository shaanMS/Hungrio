from .models import Order 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from order_payment.models import PaymentTransaction , StripeWebhookEvent
from django.http import HttpResponse ,JsonResponse
from rest_framework.views import APIView

class OrderStatusView(APIView):
 #   permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            payment = PaymentTransaction.objects.get(order=order)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if payment.status in ["pending", "processing"]:
            return Response({
                "status": "processing",
                "message": "Payment is being verified. Please wait...",
            }, status=202)

        if payment.status == "failed":
            return Response({
                "status": "failed",
                "message": "Payment failed. If amount deducted, it will be refunded.",
            })

        return Response({
            "status": "success",
            "order_id": order.id,
            "payment_id": payment.gateway_payment_id,
            "amount": order.total_amount,
            "items": order.cart_snapshot["items"],
            "invoice_available": hasattr(order, "invoice"),
        })


'''
class MyOrders()


'''