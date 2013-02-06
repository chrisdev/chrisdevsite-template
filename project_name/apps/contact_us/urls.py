from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from contact_us.views import contact_form
from contact_us.forms import MyContactForm

urlpatterns = patterns('',
    url(
        regex = r'^$',
        view  = contact_form,
        kwargs = dict(
            form_class = MyContactForm,
            template_name = 'contact_us/contact_us.html',
            success_url='/contact_us/sent/',
        ),
        name = 'contact-us',
    ),
    url(
        regex = r'^sent/$',
        view  = direct_to_template,
        kwargs = dict(
            template = 'contact_us/sent.html',
        ),
        name = 'message-sent',
    ),

    url(r"^client-project-form/$",
        direct_to_template, {"template": "contact_us/client_project_form.html"},
        name="project-form"),

)