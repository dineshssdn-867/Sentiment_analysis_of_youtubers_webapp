import pyrebase  # a library for authentication using firebase
from django.contrib import messages  # Importing messages module for showing errors
from django.contrib.auth.views import LoginView, LogoutView  # Importing login and logout views
from django.contrib.messages.views import \
    SuccessMessageMixin  # Importing successmessagemixin for showing success messages
from django.http import HttpResponseRedirect  # If any error caused it will help to redirect
from django.urls import reverse  # Used in redirecting
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView  # class based view
from .forms import RegisterForm  # importing registration form
from typing import Any, AnyStr, Dict  # Using to define the type
from decouple import config
from django.contrib.auth.models import User

firebaseConfig = {
    'apiKey': config('apikey'),
    'authDomain': config('authdomain'),
    "databaseURL": config('database'),
    'projectId': config('project_id'),
    'storageBucket': config('storagebucket'),
    'messagingSenderId': config('sender_id'),
    'appId': config('app_id'),
    'measurementId': config('measurement_id')
}

firebase = pyrebase.initialize_app(firebaseConfig)  # setting the firebase config
auth = firebase.auth()  # initializing authentication using firebase


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm  # instantiating the form object
    success_message = "Please verify your mail for the best services"  # A success message
    success_url = '/'  # Success url after registration

    def form_valid(self, form: Dict[AnyStr, Any]) -> Any:  # form validations
        username = form['username'].value()  # getting the email from form object
        email = form['email'].value()
        password = form['password1'].value()  # getting the password from form object
        print(email)
        try:  # some basic validation of e-mail
            user = auth.create_user_with_email_and_password(email,
                                                            password)  # create the object using e-mail and password
            login = auth.sign_in_with_email_and_password(email, password)  # login with e-mail and password
            auth.send_email_verification(login['idToken'])  # send the verification mail to the e-mail
            return super().form_valid(form)  # calling the form object of create view
        except:
            messages.error(self.request,
                           'E-mail is already taken please enter a new e-mail')  # adding the errors in messages list which will be shown in message.html template
            return HttpResponseRedirect(reverse('users:register'))  # Redirecting to form page if there are any errors


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class UserLoginView(LoginView):  # Initializing template for login view
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form['username'].value()  # getting the email from form object
        password = form['password'].value()  # getting the password from form object
        email = User.objects.filter(username=username).values('email')
        print(email)
        if email is None:
            messages.error(self.request,
                           'Please check your password and e-mail')
        else:
            email = email[0]['email']
        try:  # some basic validation of e-mail
            user = auth.sign_in_with_email_and_password(email, password)  # login with e-mail and password
            user_info = auth.get_account_info(user['idToken'])
            if user_info['users'][0]['emailVerified']:
                return super().form_valid(form)
            else:
                messages.error(self.request,
                               'Please verify your email')  # adding the errors in messages list which will be shown in message.html template
                return HttpResponseRedirect(reverse('users:login'))  # Redirecting to form page if there are any errors
        except:
            messages.error(self.request,
                           'Please check your password and e-mail')  # adding the errors in messages list which will be shown in message.html template
            return HttpResponseRedirect(reverse('users:login'))  # Redirecting to form page if there are any errors


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class UserLogoutView(LogoutView):  # Initializing template for logout view
    template_name = 'users/login.html'
