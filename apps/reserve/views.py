from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseNotFound, JsonResponse, Http404

from .models import SchoolBusWeekSchedules, SchoolBusTimeSchedules, SchoolBus
from .models import SchoolBusReserve as Reserve
from users.models import UcenterReserveWrapper


class SchoolBusReserve(LoginRequiredMixin, TemplateView):
    '''
    校车预约模块
    '''
    template_name = 'reserve/school-bus.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self

        week = int(timezone.now().weekday() + 1)
        ws = SchoolBusWeekSchedules.objects.get(week=week)
        times = []
        for t in ws.time.all():
            if timezone.now().strftime('%H:%M') <= t.date_schedule:
                times.append(t)
        kwargs['times'] = sorted(times, key=lambda x: x.date_schedule)
        # 依据时间重排序
        # Template上下文：目前的班次，用于渲染选择select下的option班次列表
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        now = Reserve.objects.filter(user=request.user, is_done=False)
        if now:
            context['nowpk'] = now[0].pk
        # 判断当前用户有无进行中预约
        return self.render_to_response(context)

    def post(self, request):
        '''
        处理用户的校车预约申请
        :return: 正常：序列化的SchoolBusReserve，JSON 错误：{status: 1}
        '''
        try:
            ts = SchoolBusTimeSchedules.objects.get(pk=int(request.POST.get('pk', False)))
        except:
            return HttpResponseNotFound()

        b = SchoolBus.objects.filter(schedule=ts)[0]
        if Reserve.objects.filter(user=request.user, is_done=False):
            return JsonResponse({
                'status': 0
            })

        r = Reserve.objects.create(user=request.user, schoolbus=b, is_done=False)
        return JsonResponse({
            'pk': r.pk,
            'status': 1,
            'reserve_time': r.date_reserve,
            'schedule': r.schoolbus.schedule.date_schedule
        })


class SchoolBusReserveSuccess(LoginRequiredMixin, DetailView):
    '''
    校车预约成功模块
    主要处理取消以及已乘坐操作
    '''
    template_name = 'reserve/school-bus-success.html'
    model = Reserve
    context_object_name = 'reserve'

    def check_object(self, request, obj):
        '''
        检查SchoolBusReserve的属主user是否是当前用户，权限控制
        :param request: HttpRequest
        :param obj: 检查SchoolBusReserve的属主user是否是当前用户
        :return: pass or 抛出404错误
        '''
        if request.user == obj.user:
            pass
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_object(request, self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        '''
        通过HTTP DELETE方法处理取消预约
        '''
        object = self.get_object()
        self.check_object(request, object)
        object.schoolbus.num_reserve = object.schoolbus.num_reserve - 1
        object.schoolbus.save()
        object.delete()
        return JsonResponse({
            'status': 1
        })

    def put(self, request, *args, **kwargs):
        '''
        通过HTTP PUT方法更新用户的已乘坐信息
        '''
        object = self.get_object()
        self.check_object(request, object)
        object.is_done = True
        object.save()
        # TODO :是否需要对完成做时间限制？
        return JsonResponse({
            'status': 1
        })


class GetSeatsInfo(LoginRequiredMixin, View):
    '''
    取得班次座位信息模块
    配合前端的Ajax请求
    '''
    raise_exception = True

    def post(self, request):
        '''
        :return: 序列化的SchoolBus，JSON
        '''
        try:
            ts = SchoolBusTimeSchedules.objects.get(pk=int(request.POST.get('pk', False)))
        except:
            return HttpResponseNotFound()
        b = SchoolBus.objects.filter(schedule=ts)[0]

        return JsonResponse({
            'num_seats': b.num_seats,
            'num_reserve': b.num_reserve,
            'remain': b.num_seats - b.num_reserve
        })


# Signals处理
# 类钩子方法以及回调函数
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Reserve)
def auto_wrapper(sender, **kwargs):
    user, pk, status = kwargs['instance'].user, kwargs['instance'].pk, kwargs['instance'].is_done
    urw, created = UcenterReserveWrapper.objects.get_or_create(user=user, reserve_pk=pk, reserve_type=1)
    urw.reserve_status = status
    urw.save()

