from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class UcenterView(LoginRequiredMixin, TemplateView):
    template_name = 'ucenter/ucenter.html'