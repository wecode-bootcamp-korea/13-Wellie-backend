import os
import re
import jwt
import json
import bcrypt
import datetime
import requests

from twilio.rest      import Client
from random           import randint
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from user.utils       import login_decorator
from my_settings      import SECRET
from user.models      import (
    User,
    PhoneCheck,
    UserToSubscribe
)

class DuplicatecheckView(View):
    def get(self, request) : 
        try :
            name = request.GET['nickname']
            if User.objects.filter(name = name).exists():
                return JsonResponse({"MESSAGE": "FAIL"}, status=401)
            else :
                return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)

class SignupView(View) :

    def post(self, request) :
        try :
            data   = json.loads(request.body)
            name   = data['nickName']
            mobile = data['userCell']

            if User.objects.filter(usertype=1, mobile=mobile).exists():
                return JsonResponse({"MESSAGE": "EXISTS_MOBILE"}, status=401)

            if not re.match("^(?=.{8,16})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$", data["password"]):
                return JsonResponse({"MESSAGE": "Invalid_PASSWORD"}, status=400)   

            if not re.match("^01(0|1|6|7|8|9)([0-9]{3,4})([0-9]{4})$", mobile):
                return JsonResponse({"MESSAGE": "Invalid_MOBILE"}, status=400)

            User.objects.create(
                name        = name,
                mobile      = mobile,
                password    = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                usertype_id = 1,
                shelf_name  = f'{name}의 서재'
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except TypeError :
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class SocialSignupView(View) :

    def post(self, request) :
        try :
            data        = json.loads(request.body)
            usertype    = data['userType']
            name        = data['nickName']
            social_type = {
                2 : {
                    'name'      : 'Kakao',
                    'endpoint'  : 'https://kapi.kakao.com/v2/user/me',
                    'social_id' : 'id'
                } ,
                5 : {
                    'name'      : 'Google',
                    'endpoint'  : 'https://www.googleapis.com/oauth2/v3/userinfo',
                    'social_id' : 'sub'
                }
            }

            if usertype in social_type :
                access_token    = request.headers.get('Authorization')
                profile_request = requests.get(
                    social_type[usertype]['endpoint'] , headers={"Authorization" : f"Bearer {access_token}"},
                )
                profile_json    = profile_request.json()
                social_id       = profile_json.get(social_type[usertype]['social_id'])
                if not social_id :
                    return JsonResponse({"MESSAGE": "INVALID_Token"}, status=400)
                if User.objects.filter(usertype=usertype, social_id=social_id).exists():
                    return JsonResponse({"MESSAGE": "EXISTS_Social_Id"}, status=401)
            else : 
                return JsonResponse({"MESSAGE": "INVALID_UserType"}, status=400)

            User.objects.create(
                social_id   = social_id,
                name        = name,
                usertype_id = usertype,
                shelf_name  = f'{name}의 서재'
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except TypeError :
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class LoginView(View) :

    def post(self, request) :
        try :
            data     = json.loads(request.body)
            mobile   = data['userCell']
            password = data['password']
            user = User.objects.get(usertype_id = 1, mobile = mobile)
            if not bcrypt.checkpw(password.encode("UTF-8"), user.password.encode("UTF-8")) :
                return JsonResponse({"MESSAGE": "INVALID_INPUT"}, status=401)

            token = jwt.encode(
                {"user_id": user.id},
                SECRET["secret"],
                algorithm=SECRET["algorithm"]
            )
            return JsonResponse({"MESSAGE": "SUCCESS", "Authorization": token.decode("UTF-8"), "SUBSCRIBE" : user.subscribe.exists() }, status=200)

        except User.DoesNotExist : 
            return JsonResponse({'MESSAGE': 'Signup_First'}, status=401)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except TypeError :
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class SocialLoginView(View) :

    def post(self, request) :
        try :
            data     = json.loads(request.body)
            usertype = data['userType']
            social_type = {
                2 : {
                    'name'      : 'Kakao',
                    'endpoint'  : 'https://kapi.kakao.com/v2/user/me',
                    'social_id' : 'id'
                } ,
                5 : {
                    'name'      : 'Google',
                    'endpoint'  : 'https://www.googleapis.com/oauth2/v3/userinfo',
                    'social_id' : 'sub'
                }
            }

            if usertype in social_type :
                access_token    = request.headers.get('Authorization')
                profile_request = requests.get(
                    social_type[usertype]['endpoint'] , headers={"Authorization" : f"Bearer {access_token}"},
                )
                profile_json    = profile_request.json()
                social_id       = profile_json.get(social_type[usertype]['social_id'])
                if not social_id :
                    return JsonResponse({"MESSAGE": "INVALID_Token"}, status=401)
                user = User.objects.get(usertype_id=usertype, social_id=social_id)
            else :
                return JsonResponse({"MESSAGE": "INVALID_UserType"}, status=400)

            token = jwt.encode(
                {"user_id": user.id},
                SECRET["secret"],
                algorithm=SECRET["algorithm"]
            )
            return JsonResponse({"MESSAGE": "SUCCESS", "Authorization": token.decode("UTF-8"), "SUBSCRIBE" : user.subscribe.exists() }, status=200)
        
        except User.DoesNotExist : 
            return JsonResponse({'MESSAGE': 'Signup_First'}, status=401)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except TypeError :
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class MessageSendView(View) :

    def post(self, request) :
        data        = json.loads(request.body)
        phonenumber = data['userCell']
        try : 
            if re.match("^01(0|1|6|7|8|9)([0-9]{3,4})([0-9]{4})$", phonenumber) :
                to_number  = '+82'+ phonenumber[1:]
            else :
                return JsonResponse({'MESSAGE': 'Invalid_MOBILE'}, status=401)
            
            check_number = randint(100000,999999)
            account_sid  = os.environ['TWILIO_ACCOUNT_SID']
            auth_token   = os.environ['TWILIO_AUTH_TOKEN']
            client       = Client(account_sid, auth_token)
            phonecheck   = PhoneCheck.objects.get_or_create(check_id = data['userCell'])
            phonecheck[0].check_number = check_number
            phonecheck[0].save()
            message = client.messages.create(
                    body  = f'Wellie의 서재 인증을 위해 [{check_number}]을 입력해주세요.',
                    from_ = '+12056065675',
                    to    = to_number
                )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except TypeError :
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class MessageCheckView(View) :

    def post(self, request) :
        try : 
            data         = json.loads(request.body)
            check_id     = data['userCell']
            check_number = data['codeInput']
            phonecheck   = PhoneCheck.objects.get(check_id=check_id) 
            if phonecheck.check_number == check_number :
                phonecheck.delete()
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            else :
                return JsonResponse({'MESSAGE': 'FAIL'}, status=401)
        except PhoneCheck.DoesNotExist : 
            return JsonResponse({'MESSAGE': 'Request Check Message'}, status=400)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class SubscribeView(View) :

    @login_decorator
    def post(self, request) :
        try : 
            user_id = request.user.id
            UserToSubscribe.objects.create(user_id=user_id, subscribe_id= 1)
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
        except :
            return JsonResponse({'MESSAGE': 'Already subscribed'}, status=401)