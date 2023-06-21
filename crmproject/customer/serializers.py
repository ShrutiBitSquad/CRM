from rest_framework import serializers
from customer.models import Customer, Representatives,UserTable,VendorsInsights,VendorsMailSent,Otp
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstname', 'lastname', 'mob']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserTableSerializer, self).create(validated_data)

    def validate(self,data):
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        email=data.get('email')
        password=data.get('password')
        mob=str(data.get('mob'))
        if not re.match(r'^[A-Za-z]{1,30}$', firstname):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z]{1,30}$', lastname):
            raise serializers.ValidationError('Enter a valid name')
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise serializers.ValidationError('Enter a email.')
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-_=+{}[\]|\\:;<>,.?/~]).{6,}$', password):
            raise serializers.ValidationError('Enter a valid password.')
        if not mob.isdigit() or len(mob)>10 or int(mob[0])<6:
            raise serializers.ValidationError('Enter a valid mob.no.')
        return data
    
class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representatives
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    # representatives = RepresentativeSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'

    # def create(self, validated_data):
    #     representatives_data = validated_data.pop('representatives')
    #     company = Customer.objects.create(**validated_data)
    #     for rep_data in representatives_data:
    #         Representatives.objects.create(company=company, **rep_data)
    #     return company
class RepresentativesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representatives
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = CustomerSerializer(instance.company).data
        return response

class VendorsInsightsSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorsInsights
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.company is not None:
            response['company'] = CustomerSerializer(instance.company).data
        return response

class VendorsMailSentSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorsMailSent
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['represent'] = RepresentativesSerializer(instance.represent).data
        return response


class OtpVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()
    class Meta:
        model = Otp
        fields = '__all__'
    def validate_otp(self, otp):
        if otp:
            if Otp.objects.filter(otp=otp).exists():
                user_instance = UserTable.objects.get(email=self.instance["email"].lower())
                if Otp.objects.get(email=user_instance.pk):
                    return otp
                raise serializers.ValidationError('OTP does not matched')
            raise serializers.ValidationError('OTP does not exits.')
        raise serializers.ValidationError('Please generate Otp again!!!')
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField()
    class Meta:
        model = Otp
        fields = '__all__'
    def validate_email(self, email):
        user_instance = UserTable.objects.get(email=email).lower()
        print(user_instance.email)
        if Otp.objects.filter(email_id=user_instance.pk).exists():
            if Otp.objects.get(email_id=user_instance.pk):
                return email
        else:
            return serializers.ValidationError('Email does not matched')