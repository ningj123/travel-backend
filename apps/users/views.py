from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse

from .forms import LoginForm, SignupForm
from .models import User


class IndexView(TemplateView):
    template_name = 'index.html'


class UcenterView(LoginRequiredMixin, TemplateView):
    template_name = 'ucenter/ucenter.html'

    def get(self, request, *args, **kwargs):
        if request.user.usertype == 1:
            return HttpResponseRedirect(reverse('driverindex'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status': 1
                })
            else:
                return JsonResponse({
                    'status': 0
                })
        else:
            return JsonResponse({
                'status': 0
            })


class LogoutView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class SignupView(TemplateView):
    template_name = 'signup.html'

    def post(self, request):
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password']
            try:
                user = User.objects.create_user(username=username, password=password)
                return JsonResponse({
                    'status': 1
                })
            except:
                return JsonResponse({
                    'status': 0
                })

        else:
            return JsonResponse({
                'status': 0
            })
