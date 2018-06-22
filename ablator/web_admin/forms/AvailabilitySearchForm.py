from django import forms


class SearchForm(forms.Form):
    user_identity_string = forms.CharField()
