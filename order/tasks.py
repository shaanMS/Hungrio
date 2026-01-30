# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings
# from order.models import Order 
# from order_payment.models import PaymentTransaction  #always use singular namre everywhere 


# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 10})
# def send_order_confirmation_email(self , order_id , payment_id):
#     order = Order.objects.get(id=order_id)
#     payment = PaymentTransaction.objects.get(id=payment_id)
#     subject = f"Order Confirmed | Order #{order.id}"

#     message = f"""
# Hi {order.user.first_name},

# ✅ Your payment was successful!

# Order ID: {order.id}
# Order Status: {order.status}
# Payment Status: {payment.status}
# Amount Paid: ₹{order.total_amount}
# """
#     if order.email_sent:
#      print('---------------------00000000000000000000000000000000000----------------------------------------')
#      return "Email already sent"
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [order.user.email],
#         fail_silently=False,
#     )

#     return f"Email sent for order {order.id}"


from celery import shared_task
from order.models import Order
from order_payment.models import PaymentTransaction
from order.brevo import send_brevo_email


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def send_order_confirmation_email(self, order_id, payment_id):
    order = Order.objects.get(id=order_id)
    payment = PaymentTransaction.objects.get(id=payment_id)

    if order.email_sent:
        return "Email already sent"

    subject = f"Order Confirmed | Order #{order.id}"

    html_content = f"""
    <h3>Hi {order.user.first_name},</h3>

    <p>✅ <strong>Your payment was successful!</strong></p>

    <ul>
        <li><strong>Order ID:</strong> {order.id}</li>
        <li><strong>Order Status:</strong> {order.status}</li>
        <li><strong>Payment Status:</strong> {payment.status}</li>
        <li><strong>Amount Paid:</strong> ₹{order.total_amount}</li>
    </ul>

    <p>Thanks for ordering from <b>Hungrio</b> 🍔</p>
    """

    send_brevo_email(
        to_email=order.user.email,
        subject=subject,
        html_content=html_content,
    )

    order.email_sent = True
    order.save(update_fields=["email_sent"])

    return f"Brevo email sent for order {order.id}"
