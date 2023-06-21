from django.shortcuts import render
from rest_framework.response import Response
from customer.models import Customer,Representatives
from .serializers import CustomerSerializer,UserTableSerializer,RepresentativesSerializer,VendorsInsightsSerializers,VendorsMailSentSerializers
from rest_framework.views import APIView
from customer.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime,timedelta

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