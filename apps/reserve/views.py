from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseNotFound, JsonResponse

from .models import SchoolBusWeekSchedules, SchoolBusTimeSchedules, SchoolBus


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
        def sortket(a, b):
            return a.date_schedule > b.date_schedule

        kwargs['times'] = sorted(times, key=lambda x: x.date_schedule)
        return kwargs


    def post(self, request):
        try:
            ts = SchoolBusTimeSchedules.objects.get(pk=int(request.POST.get('pk', False)))
        except:
            return HttpResponseNotFound()

        b = SchoolBus.objects.filter(schedule=ts)[0]
        b.num_reserve = b.num_reserve + 1
        # TODO 完成校车预约



class  GetSeatsInfo(LoginRequiredMixin, View):
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
