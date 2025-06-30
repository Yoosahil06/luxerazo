from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('concierge/', views.concierge_view, name='concierge'),
    path('shipping/', views.shipping_view, name='shipping'),
    path('size-guide/', views.size_guide_view, name='size_guide'),
    path('care/', views.care_view, name='care'),
    path('authenticity/', views.authenticity_view, name='authenticity'),
    path('sustainability/', views.sustainability_view, name='sustainability'),
    path('careers/', views.careers_view, name='careers'),
    path('press/', views.press_view, name='press'),
    path('private-client/', views.private_client_view, name='private_client'),
    path('personal-shopping/', views.personal_shopping_view, name='personal_shopping'),
    path('vip-events/', views.vip_events_view, name='vip_events'),
    path('customization/', views.customization_view, name='customization'),
    path('authentication/', views.authentication_view, name='authentication'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('cookies/', views.cookies_view, name='cookies'),
    path('newsletter/', views.newsletter_view, name='newsletter'),
    path('delivery/', views.delivery_view, name='delivery'),
]
