import textwrap
from django import forms
from contact_form.forms import AkismetContactForm
from django.core.urlresolvers import reverse


attrs_dict = {"class": "ct", "size": "20"}

MESSAGE_CHOICES = (
    ('Subject 1', 'Subject 1'),
    ('Subject 2', 'Subject 2'),
    ('Subject 3', 'Subject 3'),
    ('Other', 'Other'),
)


class MyContactForm(AkismetContactForm):
        def __init__(self, *args, **kwargs):
            super(MyContactForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget = forms.TextInput(attrs={'placeholder': ('Your Name')})
            self.fields['email'].widget = forms.TextInput(attrs={'placeholder': ('Your Email Address')})
    
        name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs=attrs_dict),
                           label=u'Your name')

        email = forms.EmailField(widget=forms.TextInput(attrs=attrs_dict),
                            label=u'Your email address')

        message_subject = forms.ChoiceField(choices=MESSAGE_CHOICES,
                                        label=u'What do you need to know')

        body = forms.CharField(widget=forms.Textarea(),
                           label=u'Your message')

        def subject(self):
            return u"[Contact Form Site] " + self.cleaned_data["message_subject"]

        def message(self):
            return u"From: %(name)s <%(email)s>\n\n%(body)s" % self.cleaned_data
  

#class  ZAContactForm(BaseContactForm):
    #
