from django import forms

subscription_options = [
    ('1-month', '1-Month subscription ($10 USD/Mon)'),
    ('6-month', '6-Month subscription Save $10 ($50 USD/Mon)'),
    ('1-year', '1-Year subscription Save $30 ($90 USD/Mon)'),
]


class SubscriptionForm(forms.Form):
    plans = forms.ChoiceField(choices=subscription_options)