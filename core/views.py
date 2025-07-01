from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

def home_view(request):
    return render(request, 'core/home.html')

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    if request.method == 'POST':
        # Handle luxury contact form submission
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Basic validation
        if not all([first_name, last_name, email, subject, message]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'core/contact.html')
        
        # Here you would typically:
        # 1. Save to database
        # 2. Send email notification
        # 3. Integrate with CRM system
        # For now, we'll just show a success message
        
        messages.success(request, 
            f'Thank you, {first_name}! Your message has been received. '
            'Our luxury concierge team will respond within 2 hours.')
        
        # If AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Your message has been sent successfully!'
            })
    
    return render(request, 'core/contact.html')

def concierge_view(request):
    return render(request, 'concierge/index.html')

def shipping_view(request):
    return render(request, 'core/shipping.html')

def size_guide_view(request):
    return render(request, 'core/size_guide.html')

def care_view(request):
    return render(request, 'core/care.html')

def authenticity_view(request):
    return render(request, 'core/authenticity.html')

def sustainability_view(request):
    return render(request, 'core/sustainability.html')

def careers_view(request):
    return render(request, 'core/careers.html')

def press_view(request):
    return render(request, 'core/press.html')

def private_client_view(request):
    return render(request, 'core/private_client.html')

def personal_shopping_view(request):
    return render(request, 'core/personal_shopping.html')

def vip_events_view(request):
    return render(request, 'core/vip_events.html')

def customization_view(request):
    return render(request, 'core/customization.html')

def authentication_view(request):
    return render(request, 'core/authentication.html')

def privacy_view(request):
    return render(request, 'core/privacy.html')

def terms_view(request):
    return render(request, 'core/terms.html')

def cookies_view(request):
    return render(request, 'core/cookies.html')

def newsletter_view(request):
    return render(request, 'core/newsletter.html')

def delivery_view(request):
    return render(request, 'core/delivery.html')
