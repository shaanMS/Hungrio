# invoice/services/pdf.py

from decimal import Decimal
from invoice.services.pdf import generate_pdf
from django.template.loader import render_to_string
from django.conf import settings
import os
from invoice.models import Invoice
from order.models import Order

def generate_pdf(html, path):
    from weasyprint import HTML # lazy import
    HTML(string=html).write_pdf(path)
