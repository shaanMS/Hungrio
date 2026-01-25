# invoice/views.py
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Invoice

class DownloadStripeInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            invoice = Invoice.objects.get(
                order_id=order_id,
                invoice_type="STRIPE",
                order__user=request.user,
                status="GENERATED"
            )
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice nahi mila ya aapka nahi hai"}, status=404)

        if not invoice.stripe_invoice_pdf:
            return Response({"error": "PDF link Stripe se nahi mila"}, status=404)

        return HttpResponseRedirect(invoice.stripe_invoice_pdf)