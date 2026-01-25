# import stripe
# from django.conf import settings
# from invoice.models import Invoice
# from order.models import Order
# from django.db import transaction

# class StripeInvoiceService:

#     def __init__(self, order_id):
#         self.order = Order.objects.get(id=order_id)

#     def generate(self):
#         amount = self.order.total_amount  # example

#         with transaction.atomic():
#             invoice, created = Invoice.objects.get_or_create(
#                 order=self.order,
#                 invoice_type="STRIPE",
#                 defaults={
#                     "source": "STRIPE",
#                     "cgst": 0,
#                     "sgst": 0,
#                     "igst": 0,
#                     "taxable_amount": amount,
#                     "total_amount": amount,
#                     "status": "PENDING",
#                 }
#             )

#             # agar already generated hai → dobara mat banao
#             if invoice.status == "GENERATED":
#                 return invoice

#             # 🔗 Stripe invoice creation
#             stripe.api_key = settings.STRIPE_SECRET_KEY

#             stripe_invoice = stripe.Invoice.create(
#                 customer=self.order.stripe_customer_id,
#                 auto_advance=False
#             )

#             stripe.Invoice.finalize_invoice(stripe_invoice.id)

#             # DB update
#             invoice.stripe_invoice_id = stripe_invoice.id
#             invoice.stripe_invoice_pdf = stripe_invoice.invoice_pdf
#             invoice.status = "GENERATED"
#             invoice.save()

#             return invoice







# invoice/services/stripe.py
import stripe
from django.conf import settings
from django.db import transaction
from invoice.models import Invoice
from order.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeInvoiceService:
    def __init__(self, order_id):
        self.order = Order.objects.get(id=order_id)

    def generate(self):
        if not hasattr(self.order, 'stripe_customer_id') or not self.order.stripe_customer_id:
            raise ValueError(f"Order {self.order.id} mein stripe_customer_id nahi hai")

        with transaction.atomic():
            invoice_obj, created = Invoice.objects.get_or_create(
                order=self.order,
                invoice_type="STRIPE",
                defaults={"status": "PENDING"}
            )

            if invoice_obj.status == "GENERATED":
                return invoice_obj

            # Step 1: Invoice Item add karo (yeh miss mat karna)
            stripe.InvoiceItem.create(
                customer=self.order.stripe_customer_id,
                amount=int(self.order.total_amount * 100),  # paisa → cents
                currency="inr",
                description=f"Order #{self.order.id} payment",
            )

            # Step 2: Draft Invoice banao
            stripe_invoice = stripe.Invoice.create(
                customer=self.order.stripe_customer_id,
                auto_advance=False,
                collection_method="charge_automatically",  # auto charge karega
            )

            # Step 3: Finalize karo
            finalized_invoice = stripe.Invoice.finalize_invoice(stripe_invoice.id)

            # Step 4: DB mein save
            invoice_obj.stripe_invoice_id = finalized_invoice.id
            invoice_obj.stripe_invoice_pdf = finalized_invoice.invoice_pdf
            invoice_obj.invoice_number = finalized_invoice.number
            invoice_obj.status = "GENERATED"
            invoice_obj.save()

            return invoice_obj