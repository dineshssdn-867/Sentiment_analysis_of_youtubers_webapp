import pyrebase  # a library for authentication using firebase
from django.contrib import messages   # Importing messages module for showing errors
from django.contrib.auth.views import LoginView, LogoutView   # Importing login and logout views
from django.contrib.messages.views import SuccessMessageMixin  # Importing successmessagemixin for showing success messages
from django.http import HttpResponseRedirect  # If any error caused it will help to redirect
from django.urls import reverse    # Used in redirecting
from django.views.generic import CreateView  # class based view
from .forms import RegisterForm  # importing registration form
from typing import Any, AnyStr, Dict  # Using to define the type

firebaseConfig = {  # initializing the firebase config
    'apiKey': "AIzaSyBdIsGh2PaAlxRjFrSJfOb6cwxEete2YwY",
    'authDomain': "sentiment-64808.firebaseapp.com",
    'projectId': "sentiment-64808",
    'storageBucket': "sentiment-64808.appspot.com",
    'messagingSenderId': "549019010125",
    'databaseURL': "https://sentiment-64808-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'appId': "1:549019010125:web:b064e05aac034c961bc804",
    'measurementId': "G-71JP8D1W33"
}
firebase = pyrebase.initialize_app(firebaseConfig)  # setting the firebase config
auth = firebase.auth()  # initializing authentication using firebase


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm  # instantiating the form object
    success_message = "Please verify your mail for the best services"  # A success message
    success_url = '/'  # Success url after registration

    def form_valid(self, form: Dict[AnyStr, Any]) -> Any:     # form validations
        email = form['email'].value()  # getting the email from form object
        password = form['password1'].value()  # getting the password from form object
        try:  # some basic validation of e-mail
            user = auth.create_user_with_email_and_password(email, password)  # create the object using e-mail and password
            login = auth.sign_in_with_email_and_password(email, password)  # login with e-mail and password
            auth.send_email_verification(login['idToken'])  # send the verification mail to the e-mail
            return super().form_valid(form)  # calling the form object of create view
        except:
            messages.error(self.request, 'E-mail is already taken please enter a new e-mail')  # adding the errors in messages list which will be shown in message.html template
            return HttpResponseRedirect(reverse('users:register'))  # Redirecting to form page if there are any errors


class UserLoginView(LoginView):  # Initializing template for login view
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):  # Initializing template for logout view
    template_name = 'users/login.html'
