#...
from .models import *
from .forms import SubscriptionForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, redirect
from django.urls import reverse
#from . import cart

#...


@csrf_exempt
def payment_done(request, id):
    try:
        yup = payment_request.objects.get(id = id)
        if yup.paied:
            #dash bord webeditpage
            return redirect('website:webeditpage', yup.webservice.id )
        else:
            #waiting page

            return render(request, 'test/payment_done.html')
    except webservice.DoesNotExist:
        #error page 
        return render(request,'home/templatelist.html')
    


@csrf_exempt
def payment_canceled(request):
    return render(request, 'test/payment_cancelled.html')


def subscription(request):
    if request.method == 'POST':
        f = SubscriptionForm(request.POST)
        if f.is_valid():
            request.session['subscription_plan'] = request.POST.get('plans')
            return redirect('payment:process_subscription')
    else:
        f = SubscriptionForm()
        rate = exchange_rate_usd.objects.all()[0]
        br = 3500
        dr = br / float(rate.amount)

    return render(request, 'test/subscription_form.html', locals())

def process_subscription(request):

    subscription_plan = request.session.get('subscription_plan')
    host = request.get_host()

    if subscription_plan == '1-month':
        price = "10"
        billing_cycle = 1
        billing_cycle_unit = "M"
    elif subscription_plan == '6-month':
        price = "50"
        billing_cycle = 6
        billing_cycle_unit = "M"
    else:
        price = "90"
        billing_cycle = 1
        billing_cycle_unit = "Y"

    
    paypal_dict  = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,  # monthly price
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Content subscription',
        'custom': 1,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment:payment_done',1)),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment:payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'test/process_subscription.html', locals())