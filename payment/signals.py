#...
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import datetime
from .models import *


@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):
    ipn_obj = sender

    # check for Buy Now IPN
    if ipn_obj.txn_type == 'web_accept':

        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # payment was successful
            print('great!')
            order = get_object_or_404(Order, id=ipn_obj.invoice)
            if order.get_total_cost() == ipn_obj.mc_gross:
                # mark the order as paid
                order.paid = True
                order.save()

                id = ipn_obj.custom 
                user = payment_request.objects.get(id=id)
                user.paied = True
                user.save()

                pyon = payment_on.objects.get(name = "PayPal")
                paymed = payment_made.objects.create(
                    payment_on = pyon,
                    vat = user.vat,
                    amount = user.amount,
                    discount_main = user.descount,
                    webservice = user.webservice,
                    payment_type = user.payment_type,
                    info = user.info
                )

                item = payment_request_item.objects.filter(payment_request = user)
                for i in item:
                    ite = payment_made_item.objects.create(
                        total = i.total,
                        amount = i.amount,
                        qunt = i.qunt,
                        webservice = i.webservice,
                        promo_selected = i.promo_selected,
                        selected_email = i.selected_email,
                        domainname_selected = i.domainname_selected,
                        payment_made = paymed,
                        service_payment = i.service_payment,
                        name = i.name,
                        info = i.info,
                    )

                klop = user.webservice
                klop.paid = True
                klop.save()

            else:
                print("not paid what ordered ")
                user = payment_request.objects.get(id=id)
                wpaid = wrong_paid.objects.create(
                    payment_request = user,
                    webservice = user.webservice,
                    amount = order.get_total_cost(),
                    paid_amount = ipn_obj.mc_gross
                )
                #notifay wreong payment

    # check for subscription signup IPN
    elif ipn_obj.txn_type == "subscr_signup":

        # get user id and activate the account
        print("need to notifay user")
        '''
        subject = 'your service activated'

        message = 'Thanks for signing up!'

        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [user.email])

        email.send()'''

    # check for subscription payment IPN
    elif ipn_obj.txn_type == "subscr_payment":
        id = ipn_obj.custom 
        user = payment_request.objects.get(id=id)
        user.paied = True
        user.save()

        pyon = payment_on.objects.get(name = "PayPal")
        paymed = payment_made.objects.create(
            payment_on = pyon,
            vat = user.vat,
            amount = user.amount,
            discount_main = user.descount,
            webservice = user.webservice,
            payment_type = user.payment_type,
            info = user.info
        )

        item = payment_request_item.objects.filter(payment_request = user)
        for i in item:
            ite = payment_made_item.objects.create(
                total = i.total,
                amount = i.amount,
                qunt = i.qunt,
                webservice = i.webservice,
                promo_selected = i.promo_selected,
                selected_email = i.selected_email,
                domainname_selected = i.domainname_selected,
                payment_made = paymed,
                service_payment = i.service_payment,
                name = i.name,
                info = i.info,
            )

        klop = user.webservice
        klop.paid = True
        klop.save()
        

        '''
        # user.extend()  # extend the subscription

        subject = 'Your Invoice for {} is available'.format(
            datetime.strftime(datetime.now(), "%b %Y"))

        message = 'Thanks for using our service. The balance was automatically ' \
                  'charged to your credit card.'

        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [user.email])

        email.send()'''

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        pass

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        pass