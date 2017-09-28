from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseNotFound, JsonResponse, Http404, HttpResponseRedirect
from django.urls.base import reverse
from django.db.models import Q

from .models import SchoolBusWeekSchedules, SchoolBusTimeSchedules, SchoolBus, SpecialCar, Chartered, \
    SpecialCarTimeSchedule
from .models import SpecialCarTravel as Travel
from .models import SchoolBusReserve as Reserve
from users.models import UcenterReserveWrapper


class SchoolBusReserve(LoginRequiredMixin, TemplateView):
    '''
    校车预约模块
    '''
    template_name = 'reserve/school-bus.html'

    @staticmethod
    def generate_time_list():
        '''
        静态方法：依据星期以及时间创造一天中的可用班次时间表
        :return: 一天中的可用班次时间表
        '''
        week = int(timezone.now().weekday() + 1)
        ws = SchoolBusWeekSchedules.objects.get(week=week)
        times = []
        for t in ws.time.all():
            if timezone.now().strftime('%H:%M') <= t.date_schedule:
                times.append(t)
        # 依据时间重排序
        return sorted(times, key=lambda x: x.date_schedule)

    @staticmethod
    def generate_all_time_list():
        '''
        静态方法:依据星期创造一天中所有班次时间表
        :return: 一天中所有班次时间表
        '''
        week = int(timezone.now().weekday() + 1)
        ws = SchoolBusWeekSchedules.objects.get(week=week)
        times = []
        for t in ws.time.all():
            times.append(t)
        return sorted(times, key=lambda x: x.date_schedule)

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        # Template上下文：目前的班次，用于渲染选择select下的option班次列表
        kwargs['times'] = SchoolBusReserve.generate_time_list()
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # 判断当前用户有无进行中预约
        now = Reserve.objects.filter(user=request.user, is_done=False)
        if now:
            context['nowpk'] = now[0].pk
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
        :param obj: 当前SchoolBusReserve对象
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
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Reserve)
def auto_wrapper_for_reserve(sender, **kwargs):
    # SchoolBusReserve模型的save方法的信号回调函数
    # 每当一个SchoolBusReserve被创建时就会在UcenterReserveWrapper中添加一个关联
    user, pk, status = kwargs['instance'].user, kwargs['instance'].pk, kwargs['instance'].is_done
    urw, created = UcenterReserveWrapper.objects.get_or_create(user=user, reserve_pk=pk, reserve_type=1)
    urw.reserve_status = status
    urw.save()


@receiver(post_delete, sender=Reserve)
def auto_wrapper_delete_for_reserve(sender, **kwargs):
    # SchoolBusReserve模型的delete方法的信号回掉函数
    # 每当一个SchoolBusReserve被销毁时就会同步销毁在UcenterReserveWrapper中的的关联
    pk = kwargs['instance'].pk
    UcenterReserveWrapper.objects.get(reserve_pk=pk, reserve_type=1).delete()


# TODO 完成专车的Signals回调处理


class SpecialCarTravel(LoginRequiredMixin, TemplateView):
    '''
    专车出行模块
    '''
    template_name = 'reserve/special-car.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        # carnum上下文：当前可用专车数
        kwargs['carnum'] = SpecialCar.objects.filter(status=True).__len__()
        # place_list上下文：目的地列表
        kwargs['place_list'] = Travel.get_all_place()
        times = []
        for t in SpecialCarTimeSchedule.objects.filter(Q(starttime__hour__gt=timezone.now().time().hour)):
            if timezone.now().time().minute < 30:
                if t == SpecialCarTimeSchedule.objects.get(starttime__hour=timezone.now().hour + 1, starttime__minute=0):
                    continue
            else:
                if t == SpecialCarTimeSchedule.objects.get(starttime__hour=timezone.now().hour + 1, starttime__minute=30):
                    times.remove(SpecialCarTimeSchedule.objects.get(starttime__hour=timezone.now().hour + 1, starttime__minute=0))
                    continue
            times.append(t)
        kwargs['times'] = times
        return kwargs

    def get(self, request, *args, **kwargs):
        # 重置重新匹配标志
        try:
            del request.session['oldcarpk']
        except:
            pass
        context = self.get_context_data(**kwargs)
        # 判断当前用户有无进行中预约
        now = Travel.objects.filter(user=request.user, is_done=False)
        if now:
            context['nowpk'] = now[0].car.pk
        return self.render_to_response(context)

    @staticmethod
    def match(request, place, refresh=False, car_list=None):
        if car_list or refresh:
            can_match_car = car_list
        else:
            can_match_car = SpecialCar.objects.filter(status=True)

        if can_match_car:
            for car in can_match_car:
                if car.num_user < 4:
                    Travel.objects.create(user=request.user, car=car, place=place)
                    car.users.add(request.user)
                    car.num_user = car.num_user + 1
                    if car.num_user == 4:
                        car.status = False
                    car.save()
                    return {
                        'status': 1,
                        'carpk': car.pk
                    }
            return {
                'status': 0
            }
        return {
            'status': 0
        }

    def post(self, request):
        place = request.POST.get('place', False)
        if Travel.objects.filter(user=request.user, is_done=False):
            return JsonResponse({
                'status': -1
            })
        # 匹配流程
        return JsonResponse(SpecialCarTravel.match(request, place))


# TODO: 是否需要对用户行为做时间限制
class SpecialCarMatch(LoginRequiredMixin, DetailView):
    '''
    专车匹配模块
    '''
    template_name = 'reserve/special-car-match.html'
    model = SpecialCar
    context_object_name = 'carmatch'

    def check_object(self, request, obj):
        '''
        检查当前SpecialCar对象的用户中（及当前车辆的乘坐者）是否包含当前请求用户
        :param request: HttpRequest
        :param obj: 当前SpecialCar对象
        :return: 抛出Http404异常
        '''
        if not request.user in obj.users.all():
            raise Http404

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.check_object(request, self.object)
        except:
            return HttpResponseRedirect(reverse('specialcartravel'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        '''
        通过HTTP DELETE方法处理取消匹配
        '''
        obj = self.get_object()
        obj.num_user = obj.num_user - 1
        obj.users.remove(request.user)
        obj.status = True
        obj.save()
        last_travel = request.user.get_last_special_car_travel()
        last_travel.delete()
        return JsonResponse({
            'status': 1
        })

    def put(self, request, *args, **kwargs):
        '''
        通过HTTP PUT方法处理接受匹配以及撤销
        '''
        last_travel = request.user.get_last_special_car_travel()
        car = last_travel.car
        last_travel.is_accept = not last_travel.is_accept
        last_travel.save()
        for u in last_travel.car.users.all():
            if u.get_last_special_car_travel().is_accept == True:
                car.status = False
                car.save()
        return JsonResponse({
            'status': 1
        })

    def post(self, request, *args, **kwargs):
        '''
        通过HTTP POST方法处理重新匹配
        '''
        try:
            request.session['oldcarpk'] = request.session['oldcarpk']
        except:
            request.session['oldcarpk'] = []
        obj = self.get_object()
        request.session['oldcarpk'].append(obj.pk)
        can_match_car = SpecialCar.objects.filter(status=True)
        for opk in request.session['oldcarpk']:
            can_match_car = can_match_car.exclude(pk=opk)
        now_special_car_travel = request.user.get_last_special_car_travel()
        place = now_special_car_travel.place
        result = SpecialCarTravel.match(request, place, refresh=True, car_list=can_match_car)
        if result['status']:
            now_special_car_travel.delete()
            obj.num_user = obj.num_user - 1
            obj.users.remove(request.user)
            obj.status = True
            obj.save()
            return JsonResponse(result)
        else:
            return JsonResponse(result)


# Signals处理
@receiver(post_save, sender=Travel)
def auto_wrapper_for_travel(sender, **kwargs):
    # SpecialCarTravel模型的save方法的信号回调函数
    # 每当一个SpecialCarTravel被创建时就会在UcenterReserveWrapper中添加一个关联
    user, pk, status = kwargs['instance'].user, kwargs['instance'].pk, kwargs['instance'].is_done
    urw, created = UcenterReserveWrapper.objects.get_or_create(
        user=user,
        reserve_pk=pk,
        reserve_type=2,
    )
    urw.reserve_status = status
    urw.save()


@receiver(post_delete, sender=Travel)
def auto_wrapper_delete_for_travel(sender, **kwargs):
    # SpecialCarTravel模型的delete方法的信号回掉函数
    # 每当一个SpecialCarTravel被销毁时就会同步销毁在UcenterReserveWrapper中的关联
    pk = kwargs['instance'].pk
    UcenterReserveWrapper.objects.get(reserve_pk=pk, reserve_type=2).delete()


class CharteredReserve(TemplateView):
    '''
    包车模块
    '''
    template_name = 'reserve/chartered.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['chartered'] = Chartered.objects.all()[0]
        return kwargs


def auto_create_school_bus():
    '''
    自动创建当天的所有校车班次
    '''
    week = int(timezone.now().weekday() + 1)
    ws = SchoolBusWeekSchedules.objects.get(week=week)
    for ts in ws.time.all():
        SchoolBus.objects.create(schedule=ts)
