from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls.base import reverse

from users.models import Driver
from reserve.models import SchoolBus, SpecialCar
from reserve.views import SchoolBusReserve


class DriverIndexView(LoginRequiredMixin, TemplateView):
    '''
    司机管理界面首页模块
    '''
    template_name = 'drivermanage/ucenter.html'

    def get(self, request, *args, **kwargs):
        if request.user.usertype == 2:
            return HttpResponseRedirect(reverse('ucenter'))
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
        kwargs['time_list'] = SchoolBusReserve.generate_all_time_list()
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

    def put(self, request, *args, **kwargs):
        '''
        通过HTTP PUT方法处理已完成操作
        :return: 成功：{'status': 1}
        '''
        obj = self.get_object()
        for u in obj.users.all():
            u.get_last_special_car_travel().is_done = True
            u.get_last_special_car_travel().save()
            obj.users.remove(u)
        obj.status = True
        obj.num_user = 0
        obj.save()
        return JsonResponse({
            'status': 1
        })