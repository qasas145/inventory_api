import jwt
from django.conf import settings
from datetime import timedelta, datetime
import random
import string
from .models import CustomUser
from rest_framework.authentication import BaseAuthentication




def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_access_token(data) :
    token = jwt.encode({
        "exp" : datetime.now() + timedelta(minutes=5),
        **data
    }, settings.SECRET_KEY,
    algorithm="HS256"
    )

    return token

def generate_refresh_token() :

    data = jwt.encode({
        "exp" : datetime.now() + timedelta(minutes=10),
        "data" : get_random(10)
    },
    settings.SECRET_KEY,
    algorithm="HS256"
    )

    return data


def decode_jwt(bearer) :

    if not bearer :
        return None
    token = bearer[7:]

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

    if decoded :

        try :
            return CustomUser.objects.get(id = decoded['user_id'])

        except :
            return None



class Authentication(BaseAuthentication) :


    def authenticate(self, request):
        data = self.validate_request(request.headers)

        if not data :
            return None, None

        return self.get_user(data['id']), None

    
    def get_user(self,user_id) :

        try :
            user = CustomUser.objects.get(id = user_id)
            return user
        except :
            return None

    

    def validate_request(self, headers) :

        authorization = headers.get("authorization", None)

        if not authorization :
            return None
        
        token = authorization[7:]
        data = decode_jwt(token)

        if not data :
            return None
        
        if data['exp'] > datetime.now().timestamp() > data['exp'] :
            return None

        return data

        
