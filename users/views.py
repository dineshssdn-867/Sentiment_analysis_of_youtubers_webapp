from functools import lru_cache
import pyrebase
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from .forms import RegisterForm

firebaseConfig = {
  'apiKey': "AIzaSyBdIsGh2PaAlxRjFrSJfOb6cwxEete2YwY",
  'authDomain': "sentiment-64808.firebaseapp.com",
  'projectId': "sentiment-64808",
  'storageBucket': "sentiment-64808.appspot.com",
  'messagingSenderId': "549019010125",
  'databaseURL':"https://sentiment-64808-default-rtdb.asia-southeast1.firebasedatabase.app/",
  'appId':"1:549019010125:web:b064e05aac034c961bc804",
  'measurementId': "G-71JP8D1W33"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_message = "Please verify your mail for the best services"
    success_url = '/'

    @lru_cache(maxsize=None)
    def form_valid(self, form):
        email = form['email'].value()
        password = form['password1'].value()
        try:
            user = auth.create_user_with_email_and_password(email, password)
            login = auth.sign_in_with_email_and_password(email, password)
            auth.send_email_verification(login['idToken'])
            return super().form_valid(form)
        except:
            messages.error(self.request, 'E-mail is already taken please enter a new e-mail')
            return HttpResponseRedirect(reverse('users:register'))


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/login.html'