from django import forms

class ChangePasswordForm(forms.Form):
    #password_old = forms.CharField(required=True)
    password_new = forms.CharField(required=True)
    password_confirm = forms.CharField(required=True)
