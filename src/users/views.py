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
        
from .serializers import SimpleUserUpdateSubscriptionSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


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

@extend_schema(tags=['Users: Authentication and registration'])
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



@extend_schema(tags=['Users: Authentication and registration'])
class UserRegistrationAPIView(GenericAPIView, UpdateModelMixin):
    """
    Endpoint for creating simple user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    @extend_schema(summary='(T)POST registration user. Needfull permission - All users.')
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
    


@extend_schema(tags=['Users: Authentication and registration'])
class ActivateUser(GenericAPIView):
    """
    User activation and create empty subscription.
    """
    permission_classes = (AllowAny,)
    # serializer_class = None

    @extend_schema(summary='(T)GET activate new user. Needfull permission - only User.')
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
        

@extend_schema(tags=['Users: Authentication and registration'])
class UserDetailAndUpdateAPIView(RetrieveUpdateAPIView):
    """
    View for update or see data of simple user
    """
    permission_classes = (SimpleOnlyOwnerPermission,)
    serializer_class = SimpleUserSerializer

    def get_object(self):
        request_user = CustomUser.objects.filter(id=self.kwargs["pk"]).first()
        self.check_object_permissions(request=self.request, obj=request_user)
        return self.request.user
    
    @extend_schema(summary='(T)GET user data for personal cabinet. Needfull permission - only OWNER of cabinet.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(summary='(T)PUT user data for personal cabinet. Needfull permission - only OWNER of cabinet.')
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary='(T)PATCH user data for personal cabinet. Needfull permission - only OWNER of cabinet.')
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@extend_schema(tags=['Users: Authentication and registration'])
class UserChangePasswordRequestView(GenericAPIView, UpdateModelMixin):
    """
    Endpoint for change user password
    """
    permission_classes = (SimpleOnlyOwnerPermission,)
    serializer_class = UserChangePasswordRequestSerializer

    @extend_schema(summary='(T)GET request for sending user data for marking. Needfull permission - only USER.')
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
    

@extend_schema(tags=['Users: Authentication and registration'])
class SimpleUserChangePasswordView(GenericAPIView):
    """
    Change user password.
    """
    permission_classes = (AllowAny,)
    serializer_class = SimpleUserChangePasswordSerializer

    @extend_schema(summary='(T)POST for changing password. Needfull permission - only USER.')
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
# ==================SUBSCRIPTION==========LOGIC================================================
# =============================================================================================



@extend_schema(tags=['Users: Subscription'])
@extend_schema_view(put=extend_schema(exclude=True))
class SimpleUserUpdateSubscriptionView(UpdateModelMixin, GenericAPIView):
    '''
    Update subscription
    '''
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    serializer_class = SimpleUserUpdateSubscriptionSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_activated=True)
        return queryset

    @extend_schema(summary='(T)Partly update for SUBSCRIPTION. Needfull permission - all authenticated users.')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(instance, serializer.validated_data)
            response_text = f'Відомості про підписку користувача {instance.email} змінені.'
            return Response({"message": response_text})
        else:
            return Response({"message": "failed", "details": serializer.errors})



# =============================================================================================
# ==================MESSAGES==========LOGIC====================================================
# =============================================================================================



@extend_schema(tags=['Users: Messages'])
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
    

    @extend_schema(summary='(T)GET dialog (LIST) with technical support by registred user')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(summary='(T)Send message (POST) to technical support.')
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

# =============================================================================================
# ==================Notary==========LOGIC======================================================
# =============================================================================================

@extend_schema(tags=['Users: Notary logic'])
class NotaryModelViewSet(ModelViewSet):
    '''
    Notary CRUD.
    '''
    serializer_class = NotarySerializer
    permission_classes = (SimpleUserOnlyListAndRetreiveAdminAllPermission,)
    queryset = Notary.objects.all()

    @extend_schema(summary='(T)GET NOTARY. Needfull permission - SIMPLE user or ADMIN.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='(T)POST data for creating NOTARY obj. Needfull permission - ADMIN.')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(summary='(T)GET list of NOTARY. Needfull permission - SIMPLE user or ADMIN.')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(summary='(T)PUT data for updating NOTARY obj. Needfull permission - ADMIN.')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary='(T)PATCH data for partly updating NOTARY obj. Needfull permission - ADMIN.')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(summary='(T)DESTROY NOTARY obj. Needfull permission - ADMIN.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)