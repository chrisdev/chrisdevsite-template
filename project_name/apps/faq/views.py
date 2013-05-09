import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from models import Question
from forms import SubmitFAQForm

class QuestionList(ListView):

    template_name = 'faq/faq_list.html'
    queryset = Question.objects.active()
    
    def get_context_data(self, **kwargs):
    
        context = super(QuestionList, 
            self).get_context_data(**kwargs)
        # Add in the publisher
        last_update = self.get_queryset().values('updated_on'
        	).order_by('-updated_on')[0]
        	
        context['updated_on'] = last_update['updated_on']
        return context
