from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegisterSerializers

class UserRegisterView(APIView):
    def post(self,request:Request)->Response:

        serializer = UserRegisterSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  
            user_data = UserRegisterSerializers(user).data

            return Response(data=user_data,status=201)       

        return Response(status=status.HTTP_400_BAD_REQUEST)  