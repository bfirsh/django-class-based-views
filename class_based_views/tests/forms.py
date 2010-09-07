from django import forms
from models import Author

class AuthorForm(forms.ModelForm):
    name = forms.CharField()
    slug = forms.SlugField()
    
    class Meta:
        model = Author
