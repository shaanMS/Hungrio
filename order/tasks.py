from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from order.models import Order 
from order_payment.models import PaymentTransaction  #always use singular namre everywhere 


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 10})
def send_order_confirmation_email(self , order_id , payment_id):
    order = Order.objects.get(id=order_id)
    payment = PaymentTransaction.objects.get(id=payment_id)
    subject = f"Order Confirmed | Order #{order.id}"

    message = f"""
Hi {order.user.first_name},

✅ Your payment was successful!

Order ID: {order.id}
Order Status: {order.status}
Payment Status: {payment.status}
Amount Paid: ₹{order.total_amount}

View Order:
{settings.FRONTEND_URL}/order-status/{order.id}

Thank you for shopping with us!
"""
    if order.email_sent:
     return "Email already sent"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )

    return f"Email sent for order {order.id}"


