from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from main.models import CustomUser, Product

class UserSerializer(serializers.ModelSerializer):
    cpassword = serializers.CharField(write_only=True, max_length=128)
    class Meta:
        model = CustomUser
        fields = ['username','email', 'password','cpassword']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def validate(self, data):
        if data['password'] != data['cpassword']:
            raise serializers.ValidationError("The two passwords do not match.")
        return data
    
    def create(self, validated_data):
        del validated_data["cpassword"]
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['email','otp']
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
