from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,StudentSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordRestEmailSerializer,UserPasswordResetSerialzer
from rest_framework.decorators import api_view
from .models import Student, User
from django.contrib.auth import authenticate
from .renderors import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#generate the toeken manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, format=None):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration successfully registered'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            password = serializer.data['password']
            user =authenticate(email=email, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':"login successful"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"non_feild_ererors":['email or password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
    


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data= request.data,context={'user':request.user})
        
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password change successfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendPasswordRestEmailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = SendPasswordRestEmailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset link send  successfully'},status=status.HTTP_200_OK)
        

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid,token,fomart=True):
        serializer = UserPasswordResetSerialzer(data= request.data,context= {"uid":uid,"token":token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset  send  successfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
def get(reqeust,pk=None):

    if pk is None:
        all_user = Student.objects.all()
        serializes_data = StudentSerializer(all_user,many=True)

        return Response(serializes_data.data,status=status.HTTP_201_CREATED)
    else:
        pk_data = Student.query_params.get(pk=pk)
        serializes_data = StudentSerializer(pk_data,many=False)

        return Response(serializes_data)


