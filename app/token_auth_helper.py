import jwt as jwt
from datetime import datetime, timedelta, date
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Users, InvoiceData, BlacklistToken
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def create_token(token):
    return jwt.encode(token, '1311874k', algorithm='HS256')


# def decode_token(encoded_token):
#     return jwt.decode(encoded_token, '1311874k', algorithms=['HS256'])

def decode_token(token):
    try:
        # Adjust secret key and algorithm as per your settings
        decoded = jwt.decode(token, '1311874k', algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

# def get_token_data_class(self,response):
#     headers_data = response.headers['Authorization']
#     token = headers_data[7:]
#     if BlacklistToken.objects.filter(token = token).exists():
#         response = {
#             "success" : False,
#             "message" : "User session has been expired, please login again"
#         }
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return decode_token(token)

def get_token_data_class(request):
    try:
        headers_data = request.headers['Authorization']
        token = headers_data.split()[1]  # Extract token
    except (KeyError, IndexError):
        return Response({"error": "Authorization header missing or malformed"}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the token is blacklisted
    if BlacklistToken.objects.filter(token=token).exists():
        response = {
            "success": False,
            "message": "User session has expired, please login again"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Decode the token
    decoded_data = decode_token(token)
    if "error" in decoded_data:
        return Response({"error": decoded_data["error"]}, status=status.HTTP_401_UNAUTHORIZED)

    return decoded_data


# def verify_token_class(func):        
#     def decorated(self, response, *args, **kwargs):
#         try:
#             data = get_token_data_class(self, response)
#             user_id = data['user_id']
#             expiring_on = data['expiring_on']
#             current_date = str(datetime.now())
#             if current_date < expiring_on:
#                 if Users.objects.filter(user_id = user_id).count() == 1:
#                     return func(self, response, *args, **kwargs)
#                 else:
#                     context = {
#                         "status": "failed",
#                         "message": "Invalide Token",
#                         "error": "Error: User not found"
#                     }
#                     return JsonResponse(context, status=401)
#             else:
#                 context = {
#                     "status": "failed",
#                     "message": "Invalide Token",
#                     "error": "Error: Token expired"
#                 }
#                 return JsonResponse(context, status=401)
#         except Exception as e:
#             context = {
#                 "status": "failed",
#                 "message": "Invalid Token or Conflict Happens",
#                 "error": "Error: %s" % str(e)
#             }
#             return JsonResponse(context, status=401)        
#     return decorated



def verify_token_class(func):
    @wraps(func)
    def decorated(self, request, *args, **kwargs):
        data = get_token_data_class(request)
        if isinstance(data, Response):
            return data  # If `data` is a Response object, return it immediately

        try:
            user_id = data['user_id']
            expiring_on = data['expiring_on']
            current_date = str(datetime.now())

            if current_date < expiring_on:
                if Users.objects.filter(user_id=user_id).exists():
                    return func(self, request, *args, **kwargs)
                else:
                    context = {
                        "status": "failed",
                        "message": "Invalid Token",
                        "error": "Error: User not found"
                    }
                    return JsonResponse(context, status=401)
            else:
                context = {
                    "status": "failed",
                    "message": "Invalid Token",
                    "error": "Error: Token expired"
                }
                return JsonResponse(context, status=401)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

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



# @csrf_exempt
# def verify_token(func):
#     def decorated(response, *args, **kwargs):
#         try:
#             headers_data = response.headers['Authorization']
#             token = headers_data[7:]
#             data = decode_token(token)
#             user_id = data['user_id']
#             expiring_on = data['expiring_on']
#             current_date = str(datetime.now())
#             if current_date < expiring_on:
#                 data = Users.objects.filter(user_id = user_id).count()
#                 if data == 1:
#                     return func(response, *args, **kwargs)
#                 else:
#                     context = {
#                         "message": "Invalid token",
#                     }
#                     return JsonResponse(context, status=400)
#             else:
#                 context = {
#                     "message": "Token Expired",
#                 }
#                 return JsonResponse(context, status=400)
#         except Exception as e:
#             context = {
#                 "message": e,
#             }
#             return JsonResponse(context, status=400)
#     return decorated