import stripe
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from order.models import Order
from .models import PaymentTransaction , StripeWebhookEvent
from django.http import HttpResponse ,JsonResponse
import stripe
from django.conf import settings
import json
from order.tasks import send_order_confirmation_email
from invoice.tasks import generate_invoice
stripe.api_key = settings.STRIPE_SECRET_KEY


class PlaceOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        payment_mode = request.data.get("payment_mode", "stripe")

        # 🔐 ACTIVE CART
       # cart = Cart.objects.get(user=request.user, status="ACTIVE")
        print('---------------------------------')
        cart = Cart.objects.filter(
        user=request.user,
        status="ACTIVE"
        ).first()

        if not cart:
         return Response(
                  {
                  "error": "Cart already converted or empty",
                  "hint": "Order may already be created"
                  },
                   status=400
               )
        print(cart)
       
        # 🧮 CALCULATIONS
        subtotal = Decimal("0.00")
        cart_items_snapshot = []

        for item in cart.items.all():
            item_total = item.price_snapshot * item.quantity
            subtotal += item_total

            cart_items_snapshot.append({
                "product_id": str(item.product.id) if item.product else None,
                "product_name": item.product.name if item.product else "Deleted",
                "price": str(item.price_snapshot),
                "quantity": item.quantity,
                "subtotal": str(item_total)
            })

        tax = subtotal * Decimal("0.05")
        discount = Decimal("0.00")
        total = subtotal + tax - discount


#  use below or any repitiive task in any other sevrice or chain in celery 
        


        customer = stripe.Customer.create(
        email=request.user.email,
        name='not given' #request.user.get_full_name()
        )
        print('---88888888888888888--*************')
        print('\n\n\n\n')
        print('------   ',customer.id)
        print('\n\n\n\n')
        print('---88888888888888888--*************')

        # 🧾 CREATE ORDER (SNAPSHOT BASED)
        order = Order.objects.create(
            user=request.user,
            stripe_customer_id=customer.id,
            cart_snapshot={
                "items": cart_items_snapshot,
                "subtotal": str(subtotal),
                "tax": str(tax),
                "discount": str(discount),
                "total": str(total)
            },
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            total_amount=total,
            status="PAYMENT_PENDING"
        )
        
        print("✅\n\n\n ORDER CREATED, ID =", order.id,'\n\n\n\n\n')
        # 💳 PAYMENT TRANSACTION (ORDER LINKED)
        payment = PaymentTransaction.objects.create(
            user=request.user,
            order=order,
            amount=total,
            payment_gateway=payment_mode,
            status="INITIATED"
        )

        # 🔔 STRIPE PAYMENT INTENT
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # paise
            currency="inr",
            metadata={
                "order_id": str(order.id),
                "payment_id": str(payment.id)
            },
            customer=order.stripe_customer_id
        )

        # 🔄 CART LOCK
        cart.status = "CONVERTED"
        cart.save(update_fields=["status"])

        return Response({
            "order_id": order.id,
            "client_secret": intent.client_secret
        })


'''
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    event_type = event["type"]
    intent = event["data"]["object"]

    order_id = intent["metadata"].get("order_id")
    payment_id = intent["metadata"].get("payment_id")

    if event_type == "payment_intent.succeeded":
        Order.objects.filter(id=order_id).update(status="PAID")
        PaymentTransaction.objects.filter(id=payment_id).update(
            status="SUCCESS",
            gateway_payment_id=intent["id"]
        )

    elif event_type == "payment_intent.payment_failed":
        Order.objects.filter(id=order_id).update(status="FAILED")
        PaymentTransaction.objects.filter(id=payment_id).update(
            status="FAILED",
            gateway_payment_id=intent["id"]
        )

    return HttpResponse(status=200)

    '''

'''
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    print('1-----   >   ',sig_header)
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    print('2------->',endpoint_secret)
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # ✅ HANDLE EVENTS
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        print("✅ Payment succeeded:", intent["id"])

    return HttpResponse(status=200)

'''

@csrf_exempt
def stripe_webhook(request):
    print("\n\n🔔 STRIPE WEBHOOK HIT 🔔")

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    print("👉 Signature Header:", sig_header)
    print("👉 Webhook Secret:", settings.STRIPE_WEBHOOK_SECRET)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print("❌ Invalid payload:", str(e))
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        print("❌ Signature verification failed:", str(e))
        return HttpResponse(status=400)

    if StripeWebhookEvent.objects.filter(event_id=event.id).exists():
        return JsonResponse({"status": "duplicate"}, status=200)
    print("✅ Event Verified:", event["type"])
    StripeWebhookEvent.objects.create(event_id=event.id)

    # -------------------------
    # HANDLE EVENTS
    # -------------------------
    event_type = event["type"]
    intent = event["data"]["object"]

    print("👉 PaymentIntent ID:", intent.get("id"))
    print("👉 Metadata:", intent.get("metadata"))

    order_id = intent["metadata"].get("order_id")
    payment_id = intent["metadata"].get("payment_id")
    #order = Order.objects.get(id=order_id)
    print("👉 Order ID:", order_id)
    print("👉 Payment ID:", payment_id)

    if not order_id or not payment_id:
        print("❌ Missing metadata — skipping DB update")
        return HttpResponse(status=200)

    # -------------------------
    # PAYMENT SUCCESS
    # -------------------------
    if event_type == "payment_intent.succeeded":
        print("🎉 PAYMENT SUCCESS")

        Order.objects.filter(id=order_id).update(
            status="PAID"
        )

        PaymentTransaction.objects.filter(id=payment_id).update(
            status="SUCCESS",
            gateway_payment_id=intent["id"]
        )

        print("✅ Order & Payment updated in DB")
        send_order_confirmation_email(order_id,payment_id)
        print("*******************************************")
       #generating invoice
        generate_invoice.delay(order_id)
    # -------------------------
    # PAYMENT FAILED
    # -------------------------
    elif event_type == "payment_intent.payment_failed":
        print("❌ PAYMENT FAILED")

        Order.objects.filter(id=order_id).update(
            status="FAILED"
        )

        PaymentTransaction.objects.filter(id=payment_id).update(
            status="FAILED",
            gateway_payment_id=intent["id"]
        )

        print("⚠ Order & Payment marked FAILED")

    else:
        print("ℹ Ignored event:", event_type)

    return HttpResponse(status=200)





'''

@csrf_exempt
def payment_webhook(request):
    payload = request.body
    signature = request.headers.get("X-Signature")

    if not verify_signature(payload, signature):
        return HttpResponse(status=400)

    data = json.loads(payload)
    payment_status = data["status"]
    order_id = data["metadata"]["order_id"]

    order = Order.objects.get(id=order_id)

    if payment_status == "succeeded":
        order.payment_status = "PAID"
        order.order_status = "CONFIRMED"
        order.save()
 
        send_order_confirmation_email(order)

    elif payment_status == "failed":
        order.payment_status = "FAILED"
        order.order_status = "FAILED"
        order.save()

    return HttpResponse(status=200)

'''
  

