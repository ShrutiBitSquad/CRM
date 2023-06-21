import genericpath
import random
from django.shortcuts import render
from rest_framework.response import Response
from crmproject.crmproject import settings
from customer.models import Customer,Representatives
from .serializers import CustomerSerializer,UserTableSerializer,RepresentativesSerializer,VendorsInsightsSerializers,VendorsMailSentSerializers,OtpVerificationSerializer
from rest_framework.views import APIView
from customer.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime,timedelta
from django.core.mail import send_mail


# Create your views here.

class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class LoginAPI(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer

class CustomerAPIView(APIView):
    def get(self,request):
        companies = Customer.objects.all()
        serializers = CustomerSerializer(companies,many = True)
        return Response(serializers.data)
    
    def post(self,request):
        serializers = CustomerSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status= 201)
        return Response({'message':'Not Registered as invlaid inputs'},serializers.errors,status=400)

class RepresentativesAPIView(APIView):
    def get(self,request):
        companies = Representatives.objects.all()
        serializers =RepresentativesSerializer(companies,many = True)
        return Response(serializers.data)
    
    def post(self,request):
        serializers = RepresentativesSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status= 201)
        return Response({'message':'Not Registered as invlaid inputs'},serializers.errors,status=400)

class VendorsInsightsAPIView(APIView):
    def get(self,request):
        companies = VendorsInsights.objects.all()
        serializers = VendorsInsightsSerializers(companies,many = True)
        return Response(serializers.data)
    
    def post(self,request):
        serializers = VendorsMailSentSerializers(data=request.data)
        if serializers.is_valid():
            vendors_mail_sent = serializers.save()  # Save VendorsMailSent object
            currentDateAndTime = datetime.now()
            currentdate = currentDateAndTime.strftime("%Y-%m-%d")
            prev_date = currentDateAndTime - timedelta(days=7)
            next_date = currentDateAndTime + timedelta(days=7)
            vendors_insights = VendorsInsights()
            vendors_insights.company = vendors_mail_sent.represent.company
            vendors_insights.prev_date = prev_date.date()
            vendors_insights.current_date = currentdate
            vendors_insights.next_date = next_date.date()
            vendors_insights.save()
            return Response(serializers.data, status=201)
        return Response(serializers.errors, status=400)

class VendorsMailSentAPIView(APIView):
    def get(self, request):
        mailsent = VendorsMailSent.objects.all()
        serializers = VendorsMailSentSerializers(mailsent,many = True)
        return Response(serializers.data)
    
    def post(self,request):
        serializers = VendorsMailSentSerializers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            vendors_insights = VendorsInsightsAPIView()
            vendors_insights.post(request)
            return Response(serializers.data,status= 201)
        return Response(serializers.errors,status=400)
    
class SentMailView(APIView):
    """Api to sent the otp to user mail  id to reset the password"""
    def post(self, request):
        """sending the otp to user mail id"""
        try:
            mail = UserTable.objects.get(email=request.data['email'].lower())
        except:
            return Response({'error': 'Email does not exits.'}, status=status.HTTP_404_NOT_FOUND )
        if Otp.objects.filter(email=mail).exists:
            Otp.objects.filter(email=mail).delete()
        otp = Otp.objects.create(email=mail)
        otp.otp = random.randint(100000, 999999)
        otp.save()
        subject = 'Reset Your Password'
        body = f'This is your OTP to reset password {otp.otp}'
        try:
            send_mail(subject, body, settings.EMAIL_HOST_USER, [mail.email], fail_silently=False)
            return Response({"status": "mail sent "}, status=status.HTTP_201_CREATED)
        except:
            return Response({"status": "An error ocured. Try again!!!"}, status=status.HTTP_400_BAD_REQUEST)
        
class OtpVerification(APIView):
    serializer_class = OtpVerificationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"otp": "verified"}, status=status.HTTP_200_OK)
        return Response({"otp": "please generate otp again"}, status=status.HTTP_400_BAD_REQUEST)
class ResetPasswordview(genericpath.UpdateAPIView):
    """Api to reset the password and storing the new password into database"""
    if OtpVerificationSerializer:
        serializer_class = SetNewPasswordSerializer
        def post(self, request, *args, **kwargs):
            """saving the new password of the user into database"""
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            request_email = request.data['email']
            user_object = UserTable.objects.get(email=request_email)
            if Otp.objects.filter(email_id=user_object.pk).exists():
                if UserTable.objects.get(email=request_email):
                    user_object.password = make_password(request.data['password'])
                    user_object.save()
                    otp_del = Otp.objects.filter(email=user_object.id)
                    otp_del.delete()
                    return Response({'status': 'password successfully changed'}, status=status.HTTP_201_CREATED)
                return Response({'status': 'An error occured'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'An error occured'}, status=status.HTTP_400_BAD_REQUEST)