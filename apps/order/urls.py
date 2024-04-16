
from django.urls import path, include
from .views import post_order, get_services, generate_invoice, confirm_order, process_order, cancel_order

app_name = 'order'

urlpatterns = [
    path('get-service/', post_order, name='post_order'),
    path('api/services/', get_services, name='get_services'),
    path('confirm-order/<pk>/', confirm_order, name='confirm_order'),
    path('generate-invoice/<pk>/', generate_invoice, name='generate_invoice'),
    path('api/process_order/<order_id>/', process_order, name='process_order'),
    path('order-cancele/<pk>/', cancel_order, name='cancel_order'),  
]
