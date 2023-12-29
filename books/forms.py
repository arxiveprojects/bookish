from django import forms
from .models import Book


class BookUpdateForm(forms.ModelForm):
    title= forms.CharField(required=False)
    description=forms.CharField(widget=forms.Textarea(attrs={"rows":2 }),required=False)

    class Meta:
        model=Book
        fields=['title','public','description']

class BookCreationForm(forms.ModelForm):
    title= forms.CharField(required=False)
    description=forms.CharField(widget=forms.Textarea(attrs={"rows":2 }),required=False)
    class Meta:
        model=Book
        fields=['title', 'public', 'description', 'pdf']


