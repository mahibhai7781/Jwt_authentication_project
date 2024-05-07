from rest_framework import serializers
from app.models import Student,User
from django.utils.encoding import smart_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs ={
            "password":{'write_only':True}
        }

    def validate(self,attrs):

        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password do not match")
            
        return attrs
        
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(max_length=255,style={'input_type':'password2'},write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password do not match")
        
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordRestEmailSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self,attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid',uid)
            token = PasswordResetTokenGenerator().make_token(user)

            print('password reset token',token)
            link = 'https://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link',link)

            #send email
            body = 'Click following link to reset password '+link
            data = {
                "subject":"Reset you password",
                "body": body,
                "to_email":user.email
            } 
            Util.send_email(data)
            return attrs
            
        else:
            raise serializers.ValidationError('you not a registered user')


class UserPasswordResetSerialzer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(max_length=255,style={'input_type':'password2'},write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')

            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError("password and confirm password do not match")
    
            id =smart_str(urlsafe_base64_decode(uid))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("token is not valid or expired")
    
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as idetifier:
            PasswordResetTokenGenerator().check_token(user,token)

            raise serializers.ValidationError('token is not valid or expired')






    



        
