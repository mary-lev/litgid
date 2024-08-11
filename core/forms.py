from django import forms
from .models import Person
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'second_name', 'family', 'pseudonym', 'viaf_id', 'viaf_name', 'viaf_id_alternative', 'wikidata_id', 'transliterated_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'family': forms.TextInput(attrs={'class': 'form-control'}),
            'pseudonym': forms.TextInput(attrs={'class': 'form-control'}),
            'viaf_id': forms.TextInput(attrs={'class': 'form-control'}),
            'viaf_name': forms.TextInput(attrs={'class': 'form-control'}),
            'viaf_id_alternative': forms.TextInput(attrs={'class': 'form-control'}),
            'wikidata_id': forms.TextInput(attrs={'class': 'form-control'}),
            'transliterated_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PersonEventForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=20)
    second_name = forms.CharField(label='Отчество', max_length=20)
    family = forms.CharField(label='Фамилия', max_length=20)


class LoginForm(AuthenticationForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин'

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted'


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2', ]:
            self.fields[fieldname].help_text = None

        self.fields['username'].label = 'Логин'

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class="btn btn-primary btn-lg btn-block"))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted'
