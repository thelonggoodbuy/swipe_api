from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings
from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import UserLoginSerializer, UserRegistrationSerializer, SimpleUserSerializer
from .tokens import user_activation_token
from .models import CustomUser



class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their
    email and password.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserLoginSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    

class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPIView(GenericAPIView, UpdateModelMixin):
    """
    Endpoint for creating simple user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer.validated_data['email'],
                        serializer.validated_data['password'],
                        serializer.validated_data['is_simple_user'])
        data = serializer.data
        user = CustomUser.objects.get(email=serializer.data['email'])
        current_site = get_current_site(request)
        subject = 'Activate my site account'
        message = render_to_string('users/email_templates/user_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        if settings.DEBUG == True:
            data['token'] = user_activation_token.make_token(user)
            data['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
            data['comment'] = 'token and uid data is only for DEBUG regime.'
        return Response(data, status=status.HTTP_201_CREATED)
    

class ActivateUser(GenericAPIView):
    """
    User activation.
    """
    permission_classes = (AllowAny,)
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and \
            user_activation_token.check_token(user, token) and \
            user.is_activated == False:

            user.activate_user()
            user.save()
            data = {'message': f'User {user.email} have been activated!'}
            return Response(data)
        else:
            data = {'message': 'The confirmation link was invalid, possibly\
                                     because it has already been used'}
            return Response(data)
        

class UserDetailAndUpdateAPIView(RetrieveUpdateAPIView):
    """
    View for update or see data of simple user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer

    def get_object(self):
        return self.request.user