from django.contrib import admin
from .models import *

admin.site.register(bank_account)
admin.site.register(auto_account)
admin.site.register(payment_request)
admin.site.register(payment_request_item)
admin.site.register(wrong_paid)
admin.site.register(notification_payment)
admin.site.register(exchange_rate_usd)

admin.site.register(payment_on)
admin.site.register(payment_made_item)
admin.site.register(discount_main)
admin.site.register(payment_made)