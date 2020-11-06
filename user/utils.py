import jwt

from django.http import JsonResponse
from my_settings import SECRET
from user.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(
                access_token,
                SECRET["secret"],
                algorithm=SECRET["algorithm"]
            )
            user = User.objects.get(id=payload['user_id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper
