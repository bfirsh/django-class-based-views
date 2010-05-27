from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField()
    slug = forms.SlugField()
