from django import template

from reserve.models import SchoolBusReserve, SpecialCarTravel

register = template.Library()


@register.simple_tag
def parse_single_reserve_wrapper_obj(obj):
    try:
        rpk = obj.reserve_pk
        rtype = obj.reserve_type
        if rtype == 1:
            s = SchoolBusReserve.objects.get(pk=rpk)
            return s
        elif rtype == 2:
            s = SpecialCarTravel.objects.get(pk=rpk)
            return s
    except:
        return None
