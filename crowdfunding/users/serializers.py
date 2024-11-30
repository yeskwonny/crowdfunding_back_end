from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': True},  
            'password': {'write_only': True, 'required': True},  
            'email': {'required': True},  
            'first_name': {'required': True}, 
            'last_name': {'required': True},  
        }
# password hashing->create user
    def create(self, validated_data):
        # print(validated_data)
        return CustomUser.objects.create_user(**validated_data)
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value