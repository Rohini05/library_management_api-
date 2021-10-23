from django.shortcuts import render
from .models import (
    MyUser,
    Library
)
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import viewsets 

from .serializers import (
    RegisterationSerializer,
    LoginSerializer,
    UserSerializer,
    LibrarySerializer
    )
from rest_framework import generics, permissions

#For Email
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import ListAPIView

User = get_user_model()

from rest_framework.authtoken.models import Token

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#Registration
@api_view(['POST',])
def registration(request):
    serializer = RegisterationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        
        account = serializer.save()
       
        data['response'] = "Successfully registered a new user."
        data['email'] = account.email
        data['contact_number'] = account.contact_number
        data['username'] = account.username
        return Response(data)
    else:
        data = serializer.errors
        return Response(data,status=400)


@api_view(['POST',])
def LoginAPI(request):
    serializer = LoginSerializer(data=request.data, context={'request': request})
    # serializer.is_valid(raise_exception=True)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        check_token =Token.objects.filter(user=user).first()
        if check_token:
            token =check_token.key
        else:
            token= Token.objects.create(user=user).key

        return Response({
            "user": UserSerializer(user, context={'request': request}).data,
             "token": token
        })
    else: 
        data=serializer.errors
        return Response(data,status=400)

class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False
        

# Same api can be use for create update delete
class createLibraryBook(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['create','update', 'partial_update', 'destroy'],
        AllowAny: ['retrieve', 'list']
    }
   
   





