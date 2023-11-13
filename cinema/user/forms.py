import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from django import forms
import datetime


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-mail',
        widget=forms.TextInput(attrs={'autofocus': True}))

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateForm(UserChangeForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'error_date': 'Дата рождения не может быть позже текущей даты',
        'error_phone': 'Неверный формат номера телефона',
        'error_number_card': 'Номер карты неверного формата',
        'duplicate_phone_number': _('Этот номер телефона уже использовался для регистрации.')
    }

    new_password1 = forms.CharField(
        label=_("New password"),
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'address', 'language', 'gender', 'phone_number',
                  'date_of_birth', 'number_card', 'town',
                  'new_password1', 'new_password2'
                  ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.RadioSelect(attrs={'class': 'icheck-primary d-inline'}),
            'gender': forms.RadioSelect(attrs={'class': 'icheck-primary d-inline'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+38(092)-222-22-22',
                                                   'class': 'form-control',
                                                   'data-mask': '+38(000)-000-00-00'}),
            'number_card': forms.TextInput(attrs={'placeholder': 'Номер вашей карты',
                                                  'class': 'form-control',
                                                  'data-mask': '0000-0000-0000-0000'}),
            'town': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth is not None:
            if date_of_birth > datetime.date.today():
                raise forms.ValidationError(
                    self.error_messages['error_date']
                )
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone = re.sub(r'\D', '', phone_number)
        if len(phone) == 0:
            phone_number = None
            return phone_number
        if re.search(r"^380[1-9]{2}\d{7}$", phone):
            return phone_number
        raise forms.ValidationError(
            self.error_messages['error_phone']
        )

    def clean_number_card(self):
        number_card = self.cleaned_data['number_card']
        card = re.sub(r'\D', '', number_card)
        if len(card) == 0:
            return number_card
        if re.search(r'^4[0-9]{12}(?:[0-9]{3})?$', card) or \
                re.search(r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$', card):
            return number_card
        raise forms.ValidationError(
            self.error_messages['error_number_card']
        )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 == '' and password2 == '':
            return password2
        if password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('new_password1') != '':
            user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user
