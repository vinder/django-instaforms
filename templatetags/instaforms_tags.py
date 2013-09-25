import logging

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404

from apps.dasforms.forms import ContactForm
from apps.dasforms.utils import get_form

register = template.Library()
logger = logging.getLogger(__name__)

@register.inclusion_tag('dasforms/inline_form.html', takes_context=True)
def render_inline_form(context, formtype):
    """Render inline form."""
    formtype = formtype.encode('utf8')

    try:
        formclass = get_form(formtype)
        form = formclass(referer, topic)
        action = reverse("dasform", kwargs={'formtype':formtype})
    except:
        logger.warning('Form class could not be found: %s' % formtype)
        form = ContactForm()
        action = reverse("dasform", kwargs={'formtype':'ContactForm'})
    senturl = reverse("sent")

    return {
        'action': action,
        'form': form,
        'formtype': formtype,
        'senturl': senturl,
    }


@register.inclusion_tag('dasforms/honeypot_field.html')
def render_honeypot_field(field_name=None):
    """
        Renders honeypot field named field_name (defaults to HONEYPOT_FIELD_NAME).
    """
    if not field_name:
        field_name = settings.HONEYPOT_FIELD_NAME
    value = getattr(settings, 'HONEYPOT_VALUE', '')
    if callable(value):
        value = value()
    return {'fieldname': field_name, 'value': value}
