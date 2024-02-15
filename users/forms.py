from django import forms


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
