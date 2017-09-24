from rest_framework import viewsets, mixins
from rest_framework.response import Response

from users.models import User
from users.forms import SignupForm
from serializer.users import UserSerializer


def simple_route(methods=['post'], **kwargs):
    def decorator(func):
        func.bind_to_methods = methods
        func.detail = False
        func.kwargs = kwargs
        return func
    return decorator


class APIUserView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @simple_route()
    def register(self, request):
        data = {
            'username': request.data.get('username', False),
            'password': request.data.get('password', False)
        }
        f = SignupForm(data)
        if f.is_valid():
            User.objects.create_user(username=f.cleaned_data['username'], password=f.cleaned_data['password'])
            return Response({
                'status': 1
            })
        else:
            return Response({
                'status': 0
            })
