from rest_framework.permissions import BasePermission, SAFE_METHODS

from user_control.authentication import decode_jwt




# SAFE_METHODS = SAFE_METHODS +("POST",)
class IsAuthenticatedCustom(BasePermission) :



    def has_permission(self, request, view):
        # '''
        
        if request.method in SAFE_METHODS :
            return True

        # '''
        try :
            auth_token = request.META.get("HTTP_AUTHORIZATION", None)
            print(auth_token)
        except :
            return False
        
        if not auth_token :
            return False

        print(auth_token)
        user = decode_jwt(auth_token)
        
        if not user :
            return False
        
        request.user = user
        return True


        

        
    def has_object_permission(self, request, view, obj):
        return request.user == obj
    