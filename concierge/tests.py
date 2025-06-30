from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ConciergeRequest

class ConciergeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_concierge_page_loads(self):
        """Test that the concierge page loads successfully"""
        response = self.client.get(reverse('concierge:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Personal Concierge Service')
    
    def test_concierge_request_creation(self):
        """Test creating a concierge request"""
        request_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'service_type': 'personal_shopping',
            'subject': 'Test Request',
            'message': 'This is a test request',
            'priority': 'low'
        }
        
        response = self.client.post(reverse('concierge:index'), request_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        
        # Check if request was created
        self.assertTrue(ConciergeRequest.objects.filter(email='test@example.com').exists())
    
    def test_concierge_request_model(self):
        """Test the ConciergeRequest model"""
        request = ConciergeRequest.objects.create(
            name='Test User',
            email='test@example.com',
            service_type='personal_shopping',
            subject='Test Request',
            message='This is a test request',
            priority='low'
        )
        
        self.assertEqual(str(request), 'Test User - personal_shopping (pending)')
        self.assertEqual(request.status, 'pending')
