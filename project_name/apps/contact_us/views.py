from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from contact_form.forms import ContactForm

def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html',
                 success_url=None,
                 success_template_name='contact_us/sent.html',
                 extra_context=None,
                 fail_silently=False):

    
    if success_url is None:
        success_url = reverse('contact_form_sent')
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        if form.is_valid():
            
            form.save(fail_silently=fail_silently)
            if request.is_ajax():
                
                return render_to_response(success_template_name,
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(success_url)
    else:
        form = form_class(request=request)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)