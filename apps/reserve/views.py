from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseNotFound, JsonResponse, Http404

from .models import SchoolBusWeekSchedules, SchoolBusTimeSchedules, SchoolBus
from .models import SchoolBusReserve as Reserve


class SchoolBusReserve(LoginRequiredMixin, TemplateView):
    template_name = 'reserve/school-bus.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self

        week = int(timezone.now().strftime('%w'))
        ws = SchoolBusWeekSchedules.objects.get(week=week)
        times = []
        for t in ws.time.all():
            if timezone.now().strftime('%H:%M') <= t.date_schedule:
                times.append(t)
        kwargs['times'] = sorted(times, key=lambda x: x.date_schedule)
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        now = Reserve.objects.filter(user=request.user, is_done=False)
        if now:
            context['nowpk'] = now[0].pk
        return self.render_to_response(context)

    def post(self, request):
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
    template_name = 'reserve/school-bus-success.html'
    model = Reserve
    context_object_name = 'reserve'

    def check_object(self, request, obj):
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
        object = self.get_object()
        self.check_object(request, object)
        object.schoolbus.num_reserve = object.schoolbus.num_reserve - 1
        object.schoolbus.save()
        object.delete()
        return JsonResponse({
            'status': 1
        })

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        self.check_object(request, object)
        object.is_done = True
        object.save()
        # TODO :是否需要对完成做时间限制？
        return JsonResponse({
            'status': 1
        })


class GetSeatsInfo(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request):
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
