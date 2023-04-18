from django.urls import path
from . import views

urlpatterns = [
    path('payment_done/<str:id>', views.payment_done, name = 'payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('subscription/', views.subscription, name='subscription'),  
    path('process_subscription/', views.process_subscription, name='process_subscription'),  
]  