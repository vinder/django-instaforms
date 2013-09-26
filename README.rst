==========
InstaForms
==========

Set your forms free. Add a django form to any view. The poor man's Wufoo.

Why instaforms?
---------------

There are many Djagno reusable apps that help you add a form to your website. Normally the form is tied to a specific view. What if you want to add a form to any existing view? Instaforms will help you solve this scenario.

No models required. Form results are emailed to the INSTAFORMS_RECIPENT_LIST.

Detailed documentation in the "docs" directory.

Quick start
-----------

1. Add "instaforms" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
          ...
          'instaforms',
        )

2. Make sure your email settings are configured in your settings.py::

        INSTAFORMS_RECIPIENT_LIST = ['you@example.com']

        EMAIL_USE_TLS = True
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_HOST_USER = 'feedback@example.com'
        EMAIL_HOST_PASSWORD = 'yourpassword'
        EMAIL_PORT = 587
        DEFAULT_FROM_EMAIL = 'feedback@example.com'
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

3. Include the instaforms URLconf in your project urls.py like this::

      url(r'^instaforms/', include('instaforms.urls')),

4. Edit the instaforms.forms module to add your own forms, default ContactForm included.

5. Use the instaforms template tag to add your form to your existing templates.

