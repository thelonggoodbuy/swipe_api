from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema



from .serializers import UserLoginSerializer, UserRegistrationSerializer,\
                    SimpleUserSerializer, UserChangePasswordRequestSerializer,\
                    SimpleUserChangePasswordSerializer, SimpleUserMessageCreateAndListSerializer,\
                    NotarySerializer
from .tokens import user_activation_token
from .models import CustomUser, Subscription, Message, Notary
from .services import SimpleOnlyOwnerPermission, SimpleUserOnlyListAndRetreiveAdminAllPermission


# =============================================================================================
# ==================AUTHENTICATION====LOGIC====================================================
# =============================================================================================

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
    User activation and create empty subscription.
    """
    permission_classes = (AllowAny,)
    # serializer_class = None

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
            current_subscription = Subscription.objects.create()
            user.subscription = current_subscription
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
    permission_classes = (SimpleOnlyOwnerPermission,)
    serializer_class = SimpleUserSerializer

    def get_object(self):
        print('====GET======')
        request_user = CustomUser.objects.filter(id=self.kwargs["pk"]).first()
        self.check_object_permissions(request=self.request, obj=request_user)
        return self.request.user


class UserChangePasswordRequestView(GenericAPIView, UpdateModelMixin):
    """
    Endpoint for change user password
    """
    permission_classes = (SimpleOnlyOwnerPermission,)
    serializer_class = UserChangePasswordRequestSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = CustomUser.objects.get(id=self.kwargs["pk"])
        current_site = get_current_site(request)
        subject = 'Ви зробили запит на зміну паролю.'
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
    

class SimpleUserChangePasswordView(GenericAPIView):
    """
    Change user password.
    """
    permission_classes = (AllowAny,)
    serializer_class = SimpleUserChangePasswordSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            if user == request.user and user_activation_token.check_token(user, token): 

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user.set_password(serializer.data['password'])
                user.save()
                data = {'message': f'Пароль користувача {user.email} було змінено!'}
                return Response(data)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            data = {'message': f'Не вдалося змінита пароль'}
            return Response(data)
        

# =============================================================================================
# ==================MESSAGES==========LOGIC====================================================
# =============================================================================================



@extend_schema(tags=['Messages'])
class MessageCreateAndListForSimpleUser(ListModelMixin, CreateModelMixin, GenericAPIView):
    '''
    Write message to tech support and GET list of 
    messages(per simple user).
    '''
    serializer_class = SimpleUserMessageCreateAndListSerializer
    permission_classes = (SimpleOnlyOwnerPermission,)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(from_user=user) | Q(to_user=user))
    
    @extend_schema(summary='GET dialog (LIST) with technical support by registred user')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(summary='Send message (POST) to technical support.')
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

# =============================================================================================
# ==================Notary==========LOGIC======================================================
# =============================================================================================

@extend_schema(tags=['Notary logic'])
class NotaryModelViewSet(ModelViewSet):
    '''
    Notary CRUD.
    '''
    serializer_class = NotarySerializer
    permission_classes = (SimpleUserOnlyListAndRetreiveAdminAllPermission,)
    queryset = Notary.objects.all()