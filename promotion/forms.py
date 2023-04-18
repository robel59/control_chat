from django import forms
from schedule.forms import EventForm
from .models import MyEvent

class MyEventForm(EventForm):
    field_x = forms.CharField(max_length=50)

    class Meta:
        model = MyEvent
        fields = '__all__'
