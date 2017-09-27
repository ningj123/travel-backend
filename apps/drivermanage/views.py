from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import Driver
from reserve.models import SchoolBus, SpecialCar
from reserve.views import SchoolBusReserve


class DriverIndexView(LoginRequiredMixin, TemplateView):
    '''
    司机管理界面首页模块
    '''
    template_name = 'drivermanage/ucenter.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # driver上下文：Driver对象
        context['driver'] = Driver.objects.get(user=request.user)
        return self.render_to_response(context)


class SchoolBusInfoManage(LoginRequiredMixin, TemplateView):
    '''
    校车预约信息模块
    '''
    template_name = 'drivermanage/school-bus.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        times = SchoolBusReserve.generate_time_list()
        ts = times[0]
        b = SchoolBus.objects.filter(schedule=ts)[0]
        # now上下文：默认显示的当前班次的信息，一个SchoolBus对象
        kwargs['now'] = b
        return kwargs


class SpecialCarInfoManage(LoginRequiredMixin, ListView):
    '''
    专车预约信息模块
    '''
    template_name = 'drivermanage/special-car.html'
    model = SpecialCar
    # special_car_list上下文：专车列表：返回所有的专车
    context_object_name = 'special_car_list'


class SpecialCarMatchInfoManage(LoginRequiredMixin, DetailView):
    '''
    （单个）专车匹配信息模块
    '''
    template_name = 'drivermanage/special-car-match.html'
    model = SpecialCar
    context_object_name = 'carmatch'



