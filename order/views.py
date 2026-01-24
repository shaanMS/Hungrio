from .models import Order , OrderItems
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PaymentTransaction , StripeWebhookEvent
from django.http import HttpResponse ,JsonResponse
from rest_framework.views import APIView

class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        payment = PaymentTransaction.objects.get(order=order)

        return Response({
            "order_id": order.id,
            "order_status": order.status,
            "payment_status": payment.status,
            "payment_id": payment.gateway_payment_id,
            "amount": order.total_amount,
            "items": order.cart_snapshot["items"],
            "invoice_available": hasattr(order, "invoice")
        })


'''
class MyOrders()


'''