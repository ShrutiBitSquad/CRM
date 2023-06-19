from rest_framework import serializers
from customer.models import Customer, Representatives,UserTable,VendorsInsights,VendorsMailSent
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstname', 'lastname', 'mob']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserTableSerializer, self).create(validated_data)
    
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

class VendorsInsightsSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorsInsights
        fields = '__all__'

class VendorsMailSentSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorsMailSent
        fields = '__all__'