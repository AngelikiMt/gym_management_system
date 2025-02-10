from django import forms

class ContactForm(forms.Form):
    recipients = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)