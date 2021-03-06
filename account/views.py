from django.contrib.auth import get_user_model
from rest_framework import status, permissions, mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import RegisterSerializer, LoginSerializer, ProfileSerializer
from .utils import send_activation_email, IsOwnerAccount

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_email(user)
            return Response('Аккаунт успешно создан', status=status.HTTP_201_CREATED)


class ActivationView(APIView):

    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Ваш аккаунт успешно активирован', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли из своего аккаунта.')


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """User profile viewset for retrieve and update"""
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerAccount]

    # def get_object(self):
    #     return self.request.user
