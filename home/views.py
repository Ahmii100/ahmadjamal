from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ContactMessage, ServiceQuote  # Added ServiceQuote import
import json
from datetime import datetime

def home_page(request):
    """Render the home page"""
    return render(request, 'home.html')

def projects_page(request):
    """Render the projects page"""
    return render(request, 'projects.html')

def skills_page(request):
    """Render the skills page"""
    return render(request, 'skills.html')

def services_page(request):
    """Render the services page"""
    return render(request, 'services.html')

def contact_page(request):
    """
    Handle contact form submissions and render contact page.
    - GET request: Show empty contact form
    - POST request: Process form data, save to database, send email, show success message
    """
    
    # Check if user submitted the form (POST request)
    if request.method == 'POST':
        # Get form data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        service = request.POST.get('service')
        message = request.POST.get('message')
        
        # Save the data to database using our ContactMessage model
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            service=service,
            message=message
        )
        
        # Prepare email content
        subject = f"📬 New Contact: {service}"
        email_message = f"""
═══════════════════════════════════════════
           NEW CONTACT FORM
═══════════════════════════════════════════

👤 NAME: {name}
📧 EMAIL: {email}
🔧 SERVICE: {service}

📝 MESSAGE:
{message}

═══════════════════════════════════════════
        """
        
        # Send email notification
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['ahmadjamalshakeel2004@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Thank you! Your message has been sent. I\'ll get back to you as soon as possible.')
        except Exception as e:
            messages.error(request, f'Message saved but email failed: {str(e)}')
            print(f"Email error: {e}")
        
        return redirect('contact')
    
    return render(request, 'contact.html')

def about_page(request):
    """Render the about page"""
    return render(request, 'about.html')


# ===== UPDATED FUNCTION FOR SERVICES PAGE QUOTES =====
@require_POST
def send_quote_email(request):
    """Handle quote requests from services page - saves to DB and sends emails"""
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Get client information
        client_email = data.get('email')
        client_name = data.get('name', client_email.split('@')[0])
        client_phone = data.get('phone', '')
        delivery_method = data.get('delivery_method', 'email')
        items = data.get('items', [])
        total = data.get('total', 0)
        
        # Validate required fields
        if not client_email:
            return JsonResponse({'success': False, 'error': 'Email is required'})
        
        if not items:
            return JsonResponse({'success': False, 'error': 'No items selected'})
        
        # Save to database
        quote = ServiceQuote.objects.create(
            customer_name=client_name,
            customer_email=client_email,
            customer_phone=client_phone,
            selected_services=items,
            total_amount=total,
            delivery_method=delivery_method
        )
        
        # Build items list as text for emails
        items_text = ""
        for item in items:
            items_text += f"• {item['name']} ({item['cat']}) - ${item['price']}\n"
        
        # Format phone number display (show if provided, otherwise show "Not provided")
        phone_display = client_phone if client_phone else "Not provided"
        
        # ---------- EMAIL TO CLIENT ----------
        client_subject = f"Your Quote from Ahmad Jamal - ${total}"
        client_message = f"""
═══════════════════════════════════════════
           YOUR QUOTE FROM AHMAD JAMAL
═══════════════════════════════════════════

Hello {client_name},

Thank you for your interest in my services. Here's your personalized quote:

{items_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL AMOUNT: ${total}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Contact Phone: {phone_display}
📧 Contact Email: {client_email}
📦 Delivery Method: {delivery_method}

Quote Reference: {quote.quote_id}
Date: {datetime.now().strftime('%B %d, %Y')}

I will review your request and get back to you within 24 hours.

Best regards,
Ahmad Jamal
Android Developer · SEO Specialist · Digital Consultant
        """
        
        send_mail(
            client_subject,
            client_message,
            settings.DEFAULT_FROM_EMAIL,
            [client_email],
            fail_silently=False,
        )
        
        # ---------- EMAIL TO ADMIN (YOU) ----------
        admin_subject = f"💰 New Quote Request - {client_name} - ${total}"
        admin_message = f"""
═══════════════════════════════════════════
           NEW QUOTE REQUEST
═══════════════════════════════════════════

Quote ID: {quote.quote_id}
👤 Client: {client_name}
📧 Email: {client_email}
📞 Phone: {phone_display}
📦 Delivery: {delivery_method}
📅 Date: {datetime.now().strftime('%B %d, %Y at %H:%M')}

SELECTED SERVICES:
{items_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: ${total}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View in admin: /admin/home/servicequote/{quote.id}/
        """
        
        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            ['ahmadjamalshakeel2004@gmail.com'],
            fail_silently=False,
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Quote sent successfully!',
            'quote_id': quote.quote_id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})