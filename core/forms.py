# core/forms.py
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import inlineformset_factory

# from core.models import People
# from core.validators import age_validator
from core.models import Post


class SignupForm(UserCreationForm):
    messages = {
        'required': 'idiot',
        'invalid': 'not cool',
    }
    # age = forms.IntegerField(required=True, help_text='Only years', validators=[MaxValueValidator(50),
    # MinValueValidator(18)])  # extra fields not in database just in form . we can use error_messages = a dict
    # variable with invalid and required option
    terms_and_conditions = forms.BooleanField(required=True, label='I accept all the terms and conditions ',
                                              # help_text="Accept all the terms and condition of this page",
                                              )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        # self.fields['terms_and_conditions'].error_messages = {'required': 'custom required message'}
        # self.fields['title'].validators.append(validate_tasty)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'dob', 'gender', 'password1', 'password2',
                  'terms_and_conditions', )
        widgets = {
            'gender': forms.RadioSelect()
        }

    def send_mail(self):
        subject = "New user"
        message = "Welcome to my club"
        sender = 'dikshant@gh.com'
        receiver = [self.cleaned_data['email'], ]
        send_mail(subject, message, sender, receiver, fail_silently=False)


class ProfileChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'bio', 'email', 'first_name', 'last_name', 'dob', 'phone_number',
                  'country', 'gender', 'avatar')
        widgets = {
            'gender': forms.RadioSelect()
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'picture', 'tag', )