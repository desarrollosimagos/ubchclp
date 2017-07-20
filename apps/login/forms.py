from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """
    Clase de donde se define los campos del formulario (`Login`)
    """
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class UserForm(UserCreationForm):
    tlf = forms.IntegerField()
    user_accion = forms.CharField()

