from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import ConciergeRequest
import json

class ConciergeView(TemplateView):
    template_name = 'concierge/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Personal Concierge Service',
            'meta_description': 'Experience personalized luxury service with Luxerazo\'s exclusive concierge. From personal shopping to VIP appointments, we cater to your every need.',
            'service_types': ConciergeRequest.SERVICE_TYPES,
            'priority_levels': ConciergeRequest.PRIORITY_CHOICES,
        })
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            # Extract form data
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone', ''),
                'service_type': request.POST.get('service_type'),
                'priority': request.POST.get('priority', 'low'),
                'subject': request.POST.get('subject'),
                'message': request.POST.get('message'),
                'budget_range': request.POST.get('budget_range', ''),
                'preferred_contact': request.POST.get('preferred_contact', 'email'),
            }
            
            # Create concierge request
            concierge_request = ConciergeRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                **data
            )
            
            messages.success(request, 
                'Your concierge request has been submitted successfully. '
                'Our luxury service team will contact you within 24 hours.'
            )
            
            return redirect('concierge:index')
            
        except Exception as e:
            messages.error(request, 
                'There was an error processing your request. '
                'Please try again or contact us directly.'
            )
            return self.get(request, *args, **kwargs)

def concierge_index(request):
    """Main concierge service page"""
    return ConciergeView.as_view()(request)

@csrf_exempt
def concierge_api(request):
    """API endpoint for concierge requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            concierge_request = ConciergeRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                service_type=data.get('service_type'),
                priority=data.get('priority', 'low'),
                subject=data.get('subject'),
                message=data.get('message'),
                budget_range=data.get('budget_range', ''),
                preferred_contact=data.get('preferred_contact', 'email'),
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Your concierge request has been submitted successfully.',
                'request_id': concierge_request.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'There was an error processing your request.'
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
