
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserAdminCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserAdminCreationForm, self).__init__(*args, **kwargs)
        self.fields['nascimento'] = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = User
        fields = ['username', 'email', 'nascimento']

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']
