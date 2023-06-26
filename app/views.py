from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView

def index(request):
    # Render the index.html template
    return render(request, 'index.html')

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = CustomAuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                # Form data is valid
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    # User is authenticated, log them in and redirect to the dashboard
                    login(request, user)
                    return redirect('dashboard')
            else:
                # Form data is invalid
                attempts_remaining = request.session.get('attempts_remaining', 3)
                attempts_remaining -= 1
                request.session['attempts_remaining'] = attempts_remaining

                if attempts_remaining == 0:
                    # Exceeded login attempt limit, send password reset email
                    messages.error(request, "You've failed to login. Please enter your email to reset your password.")
                elif attempts_remaining < 0:
                    return redirect('password_reset')
                else:
                    # Display error message with remaining login attempts
                    messages.error(request, "You can try {} more times or click 'Forgotten password' to reset it.".format(attempts_remaining))
        else:
            # GET request, render the login form
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm})
    else:
        # User is already authenticated, redirect to the home page
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
def dashboard(request):
    # Restricted view, requires login
    user_profile = request.user.userprofile
    context = {'user_profile': user_profile}
    return render(request, 'dashboard.html', context)

def log_out(request):
    # Log out the user and redirect to the login page
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    # Custom view for password reset functionality
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password_reset/done/'

    def form_valid(self, form):
        # Process password reset form data
        email = form.cleaned_data['email']
        try:
            # Check if user exists and send password reset email
            user = User.objects.get(username=email)
            message = "Email exists in the user table."
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            send_reset_email(self.request, email, reset_link)
            return super().form_valid(form)
        except User.DoesNotExist:
            message = "Sorry, we can’t find your registration details against this email."

        context = self.get_context_data(form=form, message=message)
        return self.render_to_response(context)

def send_reset_email(request, email, reset_link):
    # Send password reset email
    reset_link = request.build_absolute_uri(reset_link)
    subject = 'Password Reset'
    from_email = 'admin@leadhunter.app'
    to_email = [email]
    html_message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
    email_message = EmailMultiAlternatives(subject, body=None, from_email=from_email, to=to_email)
    email_message.attach_alternative(html_message, "text/html")
    email_message.send()

def reset_password_link_sended(request):
    # Render the Reset_link_send.html template
    return render(request, 'Reset_link_send.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # Custom view for password reset confirmation
    template_name = 'password_reset_confirm.html'
