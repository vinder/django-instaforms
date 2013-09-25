from django.conf import settings
from django.core.mail.message import EmailMessage
from django.template import loader
from django.core.exceptions import ImproperlyConfigured

import apps.dasforms.forms as forms

try:
    INSTAFORMS_RECIPIENT_LIST = getattr(settings, "INSTAFORMS_RECIPIENT_LIST")
    DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL")
except:
    raise ImproperlyConfigured("Missing instaforms settings.")

def get_form(formtype):
    """Return form model given formtype."""
    return getattr(forms, formtype)


class SendFormEmail(object):
    """Helper class to send off emails with form result."""
    def __init__(self, cleaned_data, **kwargs):
        self.cleaned_data = cleaned_data
        self.subject_template_name = 'dasforms/email_subject.txt'
        self.message_template_name = 'dasforms/email_template.txt'
        self.recipient_list = INSTAFORMS_RECIPIENT_LIST
        self.from_email = DEFAULT_FROM_EMAIL

    def get_message(self):
            return loader.render_to_string(self.message_template_name, self.get_context())

    def get_subject(self):
        subject = loader.render_to_string(self.subject_template_name, self.get_context())
        return ''.join(subject.splitlines())

    def get_context(self):
        """
        Form results to populate template.
        """
        context['cleaned_data'] = dict(**self.cleaned_data)
        return context

    def get_email_headers(self):
        """
        Subclasses can replace this method to define additional settings like
        a reply_to value.
        """
        if 'email' in self.cleaned_data.keys():
            return {'Reply-To': self.cleaned_data['email']}
        return None


    def get_message_dict(self, quantec=False):
        message_dict = {
            "from_email": self.from_email,
            "to": self.recipient_list,
            "subject": self.get_subject(),
            "body": self.get_message(),
            "connection": self.get_connection(),
        }
        headers = self.get_email_headers()
        if headers is not None:
            message_dict['headers'] = headers
        return message_dict

    def send_email(self, fail_silently=False):
        return EmailMessage(**self.get_message_dict()).send(fail_silently=fail_silently)
