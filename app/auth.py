import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users, BlacklistToken
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .token_auth_helper import create_token, verify_token_class
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer
    )


# API for User status update
class CreateUser(APIView):

    def post(self, request, format=None):
        user_name = request.data.get('user_name')
        password = request.data.get('password')

        Users.objects.create(
            user_name =user_name,
            password = password,
            user_status = 1
        )
        response = {
            "success" : True,
            "message" : "User Created successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
        
# API for user registered
class UserRegister(APIView):

    def post(self, request, format=None):
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success" : True,
                "message" : "User registered successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                if Users.objects.filter(email=email, user_status=1).exists():
                    user = Users.objects.get(email=email, user_status=1)
                    if check_password(password, user.password):
                        unique_id = uuid.uuid4()
                        unique_string = str(unique_id).replace("-","0")
                        member_token = unique_string
                        token = {
                            'user_id': user.user_id,
                            'user_token': member_token,
                            'created_on': str(datetime.now()),
                            'expiring_on': str(datetime.now() + timedelta(days=20))
                        }
                        access_token = create_token(token)
                        response = {
                            "success": True,
                            "message": "Login successful",
                            "token": access_token
                        }
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"error": "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            except Users.DoesNotExist:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):

    def post(self, request, format=None):
        email = request.data.get("email")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")

        user_data = Users.objects.get(email = email)

        if not check_password(old_password, user_data.password):
            return Response(
                {"message": "The old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != confirm_new_password:
            return Response(
                {"message": "The new passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_password == new_password:
            return Response(
                {"message": "The new password must be different from the old one."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user_data.password = make_password(new_password)
        user_data.save()

        response = {"success": True, "message": "Password Reset Successfully"}
        return Response(response, status=status.HTTP_200_OK)



class Logout(APIView):

    @verify_token_class
    def post(self, request):
        try:

            token = request.headers.get('Authorization').split()[1]

            blacklisted_token, created = BlacklistToken.objects.get_or_create(token=token)

            if created:
                return Response({"message": "Signout successful. Token has been blacklisted."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Token was already blacklisted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    