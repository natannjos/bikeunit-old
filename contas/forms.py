from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

from localflavor.br.forms import BRStateSelect, BRStateChoiceField
from localflavor.br.br_states import STATE_CHOICES

class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']

class UserRegister(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegister, self).__init__(*args, **kwargs)

    estado = BRStateChoiceField()
    cidade = forms.CharField(label='Cidade')
    sexo = forms.CharField(label='Sexo')
    nascimento = forms.DateField(label='Nascimento')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de senha', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        # fields = UserCreationForm.Meta.fields + ('estado',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas não correspondem")
        return password1

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label=("Informe seu Email"))


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("As senhas não correspondem."),
    }
    new_password1 = forms.CharField(label=("Nova Senha"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Confirme a Nova Senha"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2
