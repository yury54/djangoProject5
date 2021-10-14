from django import forms
from priem.models import Register
from django.contrib.admin import widgets
from datetime import date
from datetimewidget.widgets import DateTimeWidget

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('fio', 'subject', 'r_date', 'time', 'stol')

        widgets = {
            'r_date': DateTimeWidget(
                attrs={'id': 'date'}, usel10n=False, bootstrap_version=3,
                options={
                    'minView': 2,  # month view
                    'maxView': 3,  # year view
                    'weekStart': 1,
                    'language':'ru',
                    'todayHighlight': True,
                    'format': 'dd/mm/yyyy',
                    'daysOfWeekDisabled': [0, 2, 5, 6],
                    'startDate': date.today().strftime('%Y-%m-%d'),

                }),


        }

    fio = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), label='ФИО'
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), label="Причина обращения"
    )

    def __init__(self, *args, **kwargs) -> object:
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['time'].widget = forms.HiddenInput()
        self.fields['stol'].widget = forms.HiddenInput()


class MyDateWidgetForm(forms.Form):
    date1 = forms.DateTimeField(label = '',

        widget=DateTimeWidget(attrs={'id': 'date'}, usel10n=False, bootstrap_version=3,

                options={
                    'minView': 2,  # month view
                    'maxView': 3,  # year view
                    'weekStart': 1,
                    'language':'ru',
                    'todayHighlight': True,
                    'format': 'dd/mm/yyyy',

                    'startDate': date.today().strftime('%Y-%m-%d'),

                })
    )
    date2 = forms.DateTimeField(label='',

                                 widget=DateTimeWidget(attrs={'id': 'date'}, usel10n=False, bootstrap_version=3,

                                                       options={
                                                           'minView': 2,  # month view
                                                           'maxView': 3,  # year view
                                                           'weekStart': 1,
                                                           'language': 'ru',
                                                           'todayHighlight': True,
                                                           'format': 'dd/mm/yyyy',

                                                           'startDate': date.today().strftime('%Y-%m-%d'),

                                                       })
                                 )