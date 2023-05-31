from django import forms

class BotForm(forms.Form):
    message = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Enter your query here', 
        'class': 'form-control', 
        'style': 'width: 250px;',
    }))