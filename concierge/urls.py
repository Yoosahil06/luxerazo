from django.urls import path
from . import views

app_name = 'concierge'

urlpatterns = [
    path('', views.concierge_index, name='index'),
    path('api/', views.concierge_api, name='api'),
]
