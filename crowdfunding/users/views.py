
# Create your views here.
from django.shortcuts import render
# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from projects.permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly,IsOnlyOwner
from .models import CustomUser
from .serializers import CustomUserSerializer



class CustomUserList(APIView): 

# only admin can see all users
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()] 
        return [permissions.AllowAny()] 
    
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            #  save in db 
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )

class CustomUserDetail(APIView):
# ??? can i make a permission?
    
    permission_classes = [
        permissions.IsAuthenticated,IsOnlyOwner
    ]
   
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk):
        user = self.get_object(pk)
        # print(user)
        # print(request.user)
        if user.id != request.user.id:
            return Response(
            {"detail": "You do not have permission to modify this user."},
            status=status.HTTP_403_FORBIDDEN
            )
        serializer = CustomUserSerializer(instance=user,data=request.data)
        if serializer.is_valid():
            #  save in db 
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self,request,pk):
        user=self.get_object(pk)
        if user.id != request.user.id:
            return Response(
            {"detail": "You do not have permission to modify this user."},
            status=status.HTTP_403_FORBIDDEN
            )
        
        user.delete()
        return Response(
                {"detail": "Your account has been deleted."},
                status=status.HTTP_204_NO_CONTENT
                )
    


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(
            data=request.data,
            context={'request':request}
            )
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)

        return Response({
                'token':token.key,
                'user_id':user.id,
                'email':user.email
            })