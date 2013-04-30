from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from faq.views import faq_list
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

handler500 = "utils.views.server_error"

class HomePageView(TemplateView):
    template_name = "homepage.html"

urlpatterns = patterns("",
    url(r"^$",
        HomePageView.as_view(),
        name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^contact_us/", include("contact_us.urls")),
    url(r'^photos/', include('photos.urls')),
    url(r'^news/', include('news.urls')), url(r'^frontendadmin/', include('frontendadmin.urls')),
    url(r'^markitup/', include('markitup.urls')),
    url(r'^faq/$', faq_list, {"template_name":"faq/faq_list.html"},name='faq'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)