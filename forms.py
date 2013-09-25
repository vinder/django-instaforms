from django import forms


class ContactForm(forms.Form):
    """
    Default ContactForm.

    """
    message = forms.CharField(
        label = u'Message',
        required = True,
        widget = forms.Textarea(),
    )
    name = forms.CharField(
        label = u'Name',
        max_length=100,
        required = True,
    )
    email = forms.EmailField(
        label = u'Email',
        max_length=100,
        required = True,
    )
