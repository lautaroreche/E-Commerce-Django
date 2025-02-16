from django import forms


class FormularioNewsletter(forms.Form):
    email = forms.EmailField()
