import json, logging

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from apps.dasforms.utils import get_form, SendFormEmail


class SentPage(TemplateView):
    template_name = "sent.html"


class JsRequiredPage(TemplateView):
    template_name = "jsrequired.html"


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX (only) support to a form.
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        # Ajax only
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return HttpResponseRedirect(reverse('jsrequired'))

    def form_valid(self, form):
        """
        Compile and send result to relevant email recipients.
        """
        keys = form.cleaned_data.keys()
        try:
            result = ','.join(["%s:%s" % (k, form.cleaned_data[k]) for k in keys])
        except:
            logger = logging.getLogger('django.request')
            logger.error('FormResult could not be processed properly.')

        sfe = SendFormEmail(form.cleaned_data)
        sfe.send_email()


        if self.request.is_ajax():
            data = {
                'message': 'success',
            }
            return self.render_to_json_response(data)
        else:
            return HttpResponseRedirect(reverse('jsrequired'))


class InstaFormView(AjaxableResponseMixin, FormView):
    """
    Ajax only view.
    """

    def get(self, request, *args, **kwargs):
        """
        Render inline template tag only for form rendering.
        """
        raise Http404

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        formtype = self.kwargs.get('formtype', None)
        try:
            return get_form(formtype)
        except:
            raise Http404
