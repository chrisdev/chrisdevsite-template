from django.conf.urls.defaults import *
from django.contrib import admin
from faq.views import QuestionList

urlpatterns = patterns('',

    url (
        regex =r'^$',
        view = QuestionList.as_view(),
        name = 'faq',
        ),
)


