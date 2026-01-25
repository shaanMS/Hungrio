from celery import shared_task
from invoice.services.stripe import StripeInvoiceService
import logging

logger = logging.getLogger(__name__)

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def generate_invoice(order_id):
    try:
        service = StripeInvoiceService(order_id)
        invoice = service.generate()
        logger.info(f"Stripe invoice generated for order {order_id}: {invoice.stripe_invoice_id}")
    except Exception as e:
        logger.error(f"Invoice generation failed for order {order_id}", exc_info=True)
        # Optional: mark order or send notification