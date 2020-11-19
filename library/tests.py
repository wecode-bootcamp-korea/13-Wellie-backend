import json
import jwt

from django.test    import TestCase, Client

from my_settings    import SECRET
from user.models    import User, Usertype
from library.models import Library, Shelf, ShelfToBook
from book.models    import (
    Book,
    Publisher,
    Subcategory,
    Category,
    Author,
    BookToAuthor
)
'''
class MyBookTest(TestCase):
        
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=1, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo' )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            introduction     = 'introduction',
            publication_date = '2020-01-01',
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Library.objects.create(id=1, user_id=1, book_id =1)
        Author.objects.create(id=1, name='Kim')
        BookToAuthor.objects.create(id=1, book_id=1, author_id=1)

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        Library.objects.all().delete()
        BookToAuthor.objects.all().delete()

    def test_mybook_post_success(self):
        client = Client()
        book = {
            'book_id' : 1
        }
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.post('/library/mybook', json.dumps(book), **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_mybook_post_fail(self):
        client = Client()
        book = {
            'book_id' : 10
        }
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.post('/library/mybook', json.dumps(book), **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 401)

    def test_mybook_post_except(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        book = {
        }
        response = client.post('/library/mybook', json.dumps(book), **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE': "KEY_ERROR:'book_id'"})

    def test_mybook_get_success(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.get('/library/mybook', **{"HTTP_Authorization" : token})
        self.assertEqual(response.status_code, 200)

    def test_mybook_delete_success(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        book = { "booklist" : [1]  }
        response = client.delete('/library/mybook', json.dumps(book) , **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 204)

    def test_mybook_delete_fail(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        book = {  }
        response = client.delete('/library/mybook', json.dumps(book) , **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE': "KEY_ERROR:'booklist'"})
'''
class ShelfTest(TestCase):
        
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=1, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo' )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            introduction     = 'introduction',
            publication_date = '2020-01-01',
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Library.objects.create(id=1, user_id=1, book_id =1)
        Shelf.objects.create(id=1, user_id=1, name='shelf', index=1)
        Shelf.objects.create(id=2, user_id=1, name='shelf2', index=2)
        ShelfToBook.objects.create(id=1, book_id =1, shelf_id =1)

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Library.objects.all().delete()
        Shelf.objects.all().delete()
        ShelfToBook.objects.all().delete()

    def test_shelf_get_success(self):
        client = Client()
        token = jwt.encode({'user_id' : User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.get('/library/shelf', **{"HTTP_Authorization" : token})
        self.assertEqual(response.status_code, 200)

    def test_shelf_get_fail(self):
        client = Client()
        response = client.get('/library/shelf')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': 'INVALID_TOKEN'})

    def test_shelf_patch_success(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        shelves = { "shelves" : [[1,2],[2,1]] }
        response = client.patch('/library/shelf', json.dumps(shelves) , **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_shelf_patch_not_exist(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        shelves = { "shelves" : [[3,2],[2,1]] }
        response = client.patch('/library/shelf', json.dumps(shelves) , **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "NOT_EXIST_SHELF"})

    def test_shelf_patch_fail(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=1).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        shelves = { "shelves" : [{1:2},{2:1}] }
        response = client.patch('/library/shelf', json.dumps(shelves) , **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': "KEY_ERROR:1"})