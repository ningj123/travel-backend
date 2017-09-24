from django import template

from reserve.models import SchoolBusReserve

register = template.Library()


@register.simple_tag
def parse_single_reserve_wrapper_obj(obj):
    rpk = obj.reserve_pk
    rtype = obj.reserve_type
    if rtype == 1:
        s = SchoolBusReserve.objects.get(pk=rpk)
        return s
