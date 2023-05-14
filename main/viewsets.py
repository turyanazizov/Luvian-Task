from rest_framework import viewsets,status
from rest_framework.response import Response
from main.models import Product
from main.serializers import ProductSerializer, UserSerializer
from rest_framework.decorators import action
import random
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from .models import CustomUser, Product
from .serializers import ProductSerializer, VerifyUserSerializer
from rest_framework.views import APIView


class VerifyUserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"message":"Method not allowed!"})

    def post(self, request, *args, **kwargs):
        # get user email and OTP from request data
        email = request.data.get('email')
        otp = request.data.get('otp')
        # look up User object by email and check OTP

        _user = CustomUser.objects.filter(email=email, is_active=False)

        if _user:
            _user=_user.first()
            if _user.otp != otp:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User with this email not found'}, status=status.HTTP_404_NOT_FOUND)
        # activate user and save object
        _user.is_active = True
        _user.save()

        serializer = VerifyUserSerializer(_user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"Method not allowed!"})

    def delete_inactive_users(self):
        inactive_users=CustomUser.objects.filter(is_active=False)
        for user in inactive_users:
            user.delete()
    
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    def send_email(self,otp,recipient):
        from_email = settings.EMAIL_HOST_USER
        recipient = recipient
        subject = 'You have new email.'
        context = {
            "otp":otp
        }
        body = render_to_string('email.html',context=context)
        mail = EmailMessage(subject=subject, to=[recipient], from_email=from_email, body=body)
        mail.content_subtype = 'html'
        mail.send(fail_silently=True)

    def create(self, request, *args, **kwargs):
        self.delete_inactive_users()

        password=request.data.get('password')
        cpassword=request.data.get('cpassword')
        registercheck=request.data.get('registercheck')
        if  password != cpassword:
            return Response({'error': "Passwords are not same!"}, status=status.HTTP_400_BAD_REQUEST)
        if  registercheck == False:
            return Response({'error': "Check the registration rules!"}, status=status.HTTP_400_BAD_REQUEST)

        # generate OTP and send email to user
        email = request.data.get('email')
        otp = self.generate_otp()
        self.send_email(otp,email)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        instance.otp = otp
        instance.is_active = False
        instance.save()
        # return success response with OTP
        return Response({'message': "OTP sended successfully!"}, status=status.HTTP_200_OK)


class ProductPagination(LimitOffsetPagination):
    default_limit = 4


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    all_field_names = [field.name for field in Product._meta.get_fields() if field.model == Product]
    search_fields = all_field_names

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {
        'mehsul_adi': self.request.query_params.get('mehsul_adi'),
        'istehsalci': self.request.query_params.get('istehsalci'),
        'seriya': self.request.query_params.get('seriya'),
        'emeliyyat_sistemi': self.request.query_params.get('emeliyyat_sistemi'),
        'operativ_yaddas': self.request.query_params.get('operativ_yaddas'),
        'daxili_yaddas': self.request.query_params.get('daxili_yaddas'),
        'ekran': self.request.query_params.get('ekran'),
        'reng': self.request.query_params.get('reng'),
        'sim_kartlarin_sayi': self.request.query_params.get('sim_kartlarin_sayi'),
        }

        filters = {k: v for k, v in filters.items() if v is not None}
            # Get the min and max price values from query params
        min_price = self.request.query_params.get('minq')
        max_price = self.request.query_params.get('maxq')
        # Apply price range filter
        if min_price is not None and max_price is not None:
            return queryset.filter(qiymet__gte=min_price, qiymet__lte=max_price)
        elif min_price is not None:
            return queryset.filter(qiymet__gte=min_price)
        elif max_price is not None:
            return queryset.filter(qiymet__lte=max_price)   

        # Check if there are any filters toapply
        if not filters:
            return queryset

        # Apply filters and check if there are any results
        filtered_queryset = queryset.filter(**filters)
        if not filtered_queryset.exists():
            return queryset.none()
    
        return filtered_queryset