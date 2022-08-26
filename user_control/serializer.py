from rest_framework import serializers
from .models import CustomUser, choices, UserActivities


class CreateUserSerializer(serializers.Serializer) :
    fullname = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    password = serializers.CharField(style = {'input_type' : 'password'}, required = True, write_only = True)
    role = serializers.ChoiceField(choices=choices)


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)  
        return user

class LoginSerializer(serializers.Serializer) :
    email = serializers.EmailField(required = True)
    password = serializers.CharField(style = {'input_type' : 'password'}, required = True)


class UpdatePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()



class CustomUserSerializer(serializers.ModelSerializer) :

    class Meta :
        model = CustomUser
        exclude = ("password",)



class UserActivitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivities
        fields = ("__all__")
