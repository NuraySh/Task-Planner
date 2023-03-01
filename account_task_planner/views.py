from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import logout

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from account_task_planner.tokens import account_activation_token

from django.contrib import messages

from account_task_planner.forms import CustomUserCreationForm

from account_task_planner.models import CustomUser

from django.contrib.auth.forms import UserCreationForm

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm
    # redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('account/confirmation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(self.request, 'Your registration is successful. Please check your email to activate your account.', extra_tags='success')
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        
        return super(RegisterPage, self).get( *args, **kwargs)

    def get_success_url(self):
        # return the current URL to redirect to the same page
        return self.request.path
    

class ActivateAccount(TemplateView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # login(request, user)
            return redirect('login')
        else:
            return render(request, 'activation_failed.html')
        

def logout_view(request):
    logout(request)
    return redirect('login')





    


