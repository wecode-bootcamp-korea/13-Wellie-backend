import json
import bcrypt

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from my_settings   import SECRET
from user.models   import (
    User,
    Usertype
)

class DuplicatecheckTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile')
        User.objects.create( name = 'hello', usertype_id = 1 , shelf_name='hellllo1')

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()

    def test_duplicatecheck_get_success(self):
        client = Client()
        response = client.get('/user/check?nickname=abc')
        self.assertEqual(response.status_code, 200)

    def test_duplicatecheck_get_fail(self):
        client = Client()
        response = client.get('/user/check?nickname=hello')
        self.assertEqual(response.status_code, 401)

    def test_duplicatecheck_get_wrong_key(self):
        client = Client()
        response = client.get('/user/check?nick=hello')
        self.assertEqual(response.status_code, 400)

class SignupTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        Usertype.objects.create( id = 2, name = 'kakako' )

        User.objects.create( name = 'hello', usertype_id = 1, mobile = '01000010001' ,shelf_name= 'hellllo1')

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()

    def test_signup_post_mobile_success(self):
        client = Client()
        user = {
            'nickName' : 'hi',
            'userCell' : '01000020002',
            'password' : 'Aa12341234'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_signup_post_exists_mobile_fail(self):
        client = Client()
        user = {
            'nickName' : 'hi',
            'userCell' : '01000010001',
            'password' : 'Aa12341234'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "EXISTS_MOBILE"})

    def test_signup_post_wrong_password_fail(self):
        client = Client()
        user = {
            'nickName' : 'hi',
            'userCell' : '01000020002',
            'password' : 'aa12341234'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "Invalid_PASSWORD"})

    @patch('user.views.requests')
    def test_signup_post_kakao_success(self, mocked_request):

        class KakaoResponse:
            def json(self):
                return {
                    "id": 1234
                }

        client = Client()
        user = {
            'userType' : 2,
            'nickName' : 'hi2'
        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        response           = client.post('/user/signup/social', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 201)

    @patch('user.views.requests')
    def test_signup_post_social_fail(self, mocked_request):

        class KakaoResponse:
            def json(self):
                return {
                    "id": 1234
                }

        client = Client()
        user = {
            'userType' : 10,
            'nickName' : 'hi2'
        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        response           = client.post('/user/signup/social', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_UserType"})

    @patch('user.views.requests')
    def test_signup_post_keyerror(self, mocked_request):

        class KakaoResponse:
            def json(self):
                return {
                    "id": '1234'
                }

        client = Client()
        user = {
            'nickName' : 'hi2'
        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        response           = client.post('/user/signup/social', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': "KEY_ERROR:'userType'"})

class LoginTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        Usertype.objects.create( id = 2, name = 'kakako' )

        User.objects.create( name = 'hello', usertype_id = 1, mobile = '01000010001', password = bcrypt.hashpw("Aa123123".encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8") ,shelf_name= 'hellllo1')
        User.objects.create( name = 'hello2', usertype_id = 2, social_id = '1234' ,shelf_name= 'hellllo2' )

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()

    def test_login_post_mobile_success(self):
        client = Client()
        user = {
            'userType' : 1,
            'nickName' : 'hello',
            'userCell' : '01000010001',
            'password' : 'Aa123123'
        }
        response = client.post('/user/login', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_login_post_mobile_fail(self):
        client = Client()
        user = {
            'userType' : 1,
            'nickName' : 'hello',
            'userCell' : '01000010001',
            'password' : 'Aa1231234'
        }
        response = client.post('/user/login', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_INPUT"})

    @patch('user.views.requests')
    def test_signup_post_kakao_success(self, mocked_request):

        class KakaoResponse:
            def json(self):
                return {
                    "id": '1234'
                }

        client = Client()
        user = {
            'userType' : 2,
            'nickName' : 'hello2'
        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        response           = client.post('/user/login/social', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_signup_post_kakao_fail(self, mocked_request):

        class KakaoResponse:
            def json(self):
                return {
                    "id": '124'
                }

        client = Client()
        user = {
            'userType' : 2,
            'nickName' : 'hello2'
        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        response           = client.post('/user/login/social', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "Signup_First"})