import jwt
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Users

def create_token(token):
    return jwt.encode(token, '1311874k', algorithm='HS256')


def decode_token(encoded_token):
    return jwt.decode(encoded_token, '1311874k', algorithms=['HS256'])

def get_token_data_class(self,response):
    headers_data = response.headers['Authorization']
    token = headers_data[7:]
    return decode_token(token)

@csrf_exempt
def verify_token(func):
    def decorated(response, *args, **kwargs):
        try:
            headers_data = response.headers['Authorization']
            token = headers_data[7:]
            data = decode_token(token)
            user_id = data['user_id']
            expiring_on = data['expiring_on']
            current_date = str(datetime.now())
            if current_date < expiring_on:
                data = Users.objects.filter(user_id = user_id).count()
                if data == 1:
                    return func(response, *args, **kwargs)
                else:
                    context = {
                        "message": "Invalid token",
                    }
                    return JsonResponse(context, status=400)
            else:
                context = {
                    "message": "Token Expired",
                }
                return JsonResponse(context, status=400)
        except Exception as e:
            # print(e)
            context = {
                "message": e,
            }
            return JsonResponse(context, status=400)
    return decorated


def verify_token_class(func):        
    def decorated(self, response, *args, **kwargs):
        try:
            data = get_token_data_class(self, response)
            user_id = data['user_id']
            expiring_on = data['expiring_on']
            current_date = str(datetime.now())
            if current_date < expiring_on:
                if Users.objects.filter(user_id = user_id).count() == 1:
                    return func(self, response, *args, **kwargs)
                else:
                    context = {
                        "status": "failed",
                        "message": "Invalide Token",
                        "error": "Error: User not found"
                    }
                    return JsonResponse(context, status=401)
            else:
                context = {
                    "status": "failed",
                    "message": "Invalide Token",
                    "error": "Error: Token expired"
                }
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {
                "status": "failed",
                "message": "Invalid Token or Conflict Happens",
                "error": "Error: %s" % str(e)
            }
            return JsonResponse(context, status=401)
        
        
    return decorated