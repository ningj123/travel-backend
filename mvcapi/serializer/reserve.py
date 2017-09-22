from rest_framework import serializers
from reserve.models import SchoolBusReserve

class SchoolBusReserveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SchoolBusReserve
        fields = (
            'user',
            'schoolbus',
            'date_reserve'
        )