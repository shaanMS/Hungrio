from decimal import Decimal
from invoice.models import Invoice
from order.models import Order

# class GSTInvoiceService:
    
#     def generate(self):
#         from invoice.services.pdf import generate_pdf
#         invoice, _ = Invoice.objects.get_or_create(
#             order=self.order,
#             invoice_type="GST"
#         )

#         # calculate GST
#         # generate PDF
#         # save file

#         invoice.status = "GENERATED"
#         invoice.save()





# invoice/services/gst.py
from decimal import Decimal
from django.db import transaction
from invoice.models import Invoice
from invoice.services.pdf import generate_pdf  # your PDF generator

class GSTInvoiceService:
    def __init__(self, order_id):
        self.order = Order.objects.get(id=order_id)

    def generate(self):
        with transaction.atomic():
            invoice, _ = Invoice.objects.get_or_create(
                order=self.order,
                invoice_type="GST",
                defaults={"status": "PENDING"}
            )

            if invoice.status == "GENERATED":
                return invoice

            # Example GST calc (adjust per your rules)
            base = self.order.total_amount
            gst_rate = Decimal("0.18")          # 18% example
            gst_amount = base * gst_rate
            half = gst_amount / 2

            invoice.gstin = self.order.user.gstin or ""  # from user/profile
            invoice.hsn_code = "9983"                    # example service code
            invoice.cgst = half.quantize(Decimal("0.01"))
            invoice.sgst = half.quantize(Decimal("0.01"))
            invoice.taxable_amount = base
            invoice.total_amount = base + gst_amount

            # Generate and save PDF
            pdf_path = generate_pdf(invoice)   # returns path or File object
            invoice.pdf_file.save(f"invoice-{invoice.order.id}-GST.pdf", pdf_path)
            invoice.status = "GENERATED"
            invoice.save()

            return invoice