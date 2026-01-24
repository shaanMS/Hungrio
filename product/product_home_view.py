# product/views.py - ADD THIS FUNCTION
from django.shortcuts import render

def menu_ui(request):
    """Render the enhanced menu UI"""
    return render(request, 'index.html')