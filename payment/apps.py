from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'


class PaypalConfig(AppConfig):
    name = 'payment'

    def ready(self):
        # import signal handlers
        import payment.signals
