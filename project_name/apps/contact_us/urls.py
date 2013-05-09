from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
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
        view  = TemplateView.as_view(template_name="contact_us/sent.html"),
        name = 'message-sent',
    ),

    url(regex= r"^client-project-form/$",
        view = TemplateView.as_view(template_name="contact_us/client_project_form.html"),
        name="project-form"),

)