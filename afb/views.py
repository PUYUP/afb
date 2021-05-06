from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from afb.auth import UserModelBackend

User = get_user_model()


class LoginView(TemplateView):
    template_name = 'signin.html'

    def render_to_response(self, context, *args, **kwargs):
        response = super().render_to_response(context, *args, **kwargs)
        if self.request.user.is_authenticated:
            response = HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return response

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            userbackend = UserModelBackend()
            user = userbackend.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                user_logged_in.send(sender=User, request=request, user=user)
                messages.add_message(self.request, messages.SUCCESS, 'Logged In')
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
            else:
                messages.add_message(self.request, messages.ERROR, "User is inactive")
        else:
            messages.add_message(self.request, messages.ERROR, "Your email or password is incorrect.")
        return HttpResponseRedirect(settings.LOGIN_URL)


class LogoutView(LoginRequiredMixin, TemplateView):
    def render_to_response(self, context, *args, **kwargs):
        User = get_user_model()
        user = self.request.user
        logout(self.request)
        user_logged_out.send(sender=User, request=self.request, user=user)
        messages.add_message(self.request, messages.SUCCESS, "Logged Out")
        return HttpResponseRedirect(settings.LOGIN_URL)
