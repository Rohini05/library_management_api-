from rest_framework import serializers
from .models import MyUser,Library
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')


#Registration
class RegisterationSerializer(serializers.ModelSerializer):

    password2       = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    
    class Meta:
        model = MyUser
        fields = ['email', 'contact_number', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
       

    def save(self):
        account = MyUser(
            email=self.validated_data['email'],
            contact_number=self.validated_data['contact_number'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password Error': 'Password Does Not  Match.'})
        account.set_password(password)
        account.is_active = False
        username = account.username.title()
        account.username = username
        account.save()
        return account
        

      


#Login
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print(email)
        try:
            username = MyUser.objects.get(email=email).email
            print(username,"bsagsad")
        except User.DoesNotExist:
            username = attrs.get('email')
            print(username,"bsagsadwer3543543")

        #Check user verified or not.
        if MyUser.objects.filter(email=username):
            is_verified = MyUser.objects.get(email=username)
            if is_verified.is_active == False :
                raise serializers.ValidationError( is_verified.username + " You are not verified yet.Please check email to verify your account")


            #Then Authenticate    
            user = authenticate(username=username, password=password)

            if user and user.is_active:
                attrs['user'] = user
                return attrs
            raise serializers.ValidationError("Invalid Credentials (Click Forgot Password If You Wish To Reset).")
        else :
            raise serializers.ValidationError("You are not register yet !!!")


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"



