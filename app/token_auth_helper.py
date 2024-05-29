import jwt as jwt
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Users, InvoiceData
from rest_framework.response import Response
from rest_framework import status

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


def generate_order_no():
    current_date = date.today()
    formatted_date = str(current_date).replace('-', '')
    last_invoice  = InvoiceData.objects.filter(date = current_date).order_by('-id').first()
    if last_invoice:
        last_order_no = last_invoice.order_no
        try:
            base_order_no, last_sequence = last_order_no.split('/')
            new_sequence = int(last_sequence) + 1
        except ValueError:
            new_sequence = 1
    else:
        new_sequence = 1
    new_order_no = f"{formatted_date}/{new_sequence}"
    return new_order_no