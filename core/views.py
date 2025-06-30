from django.shortcuts import render

def home_view(request):
    return render(request, 'core/home.html')

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
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
