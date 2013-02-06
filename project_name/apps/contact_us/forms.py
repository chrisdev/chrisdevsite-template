import textwrap
from django import forms
from contact_form.forms import AkismetContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit, Fieldset
from django.core.urlresolvers import reverse


attrs_dict = {"class": "ct", "size": "20"}

MESSAGE_CHOICES = (
    ('Subject 1', 'Subject 1'),
    ('Subject 2', 'Subject 2'),
    ('Subject 3', 'Subject 3'),
    ('Saying HI', 'Just saying Hi!')
)


class MyContactForm(AkismetContactForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'contact-form'
        self.helper.form_class = "nice custom"
        self.helper.form_method = "post"
        self.helper.form_action = "contact-us"

        self.helper.layout = Layout(
            Fieldset("Contact Form", "name", "email", "message_subject", "body"),
            Submit('send', 'Send It >>',
                   css_class='button medium radius nice black'),

        )

        super(MyContactForm, self).__init__(*args, **kwargs)

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
