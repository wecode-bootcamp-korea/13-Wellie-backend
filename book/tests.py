import json
import jwt

from django.test    import TestCase, Client

from my_settings    import SECRET
from user.models    import User, Usertype
from library.models import Library
from book.models    import (
    Book,
    Publisher,
    Subcategory,
    Category,
    Author,
    Comment,
    CommentLike,
    BookToAuthor
)

class BookDetailTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=12, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo' )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Library.objects.create(id=1, user_id=12, book_id =1)
        Comment.objects.create(id=1, user_id=12, book_id =1, content='content')
        CommentLike.objects.create(id=1, user_id=12, comment_id =1)
        Author.objects.create(id=1, name='Kim')
        Author.objects.create(id=2, name='Lee')
        BookToAuthor.objects.create(id=1, book_id=1, author_id=2)

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        Library.objects.all().delete()
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()
        BookToAuthor.objects.all().delete()

    def test_BookDetail_get_success(self):
        client = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.get('/book/1', **{"HTTP_Authorization" : token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "MESSAGE": {
                "user_name" : 'hello2',
                "book_id": 1,
                "title": "title",
                "image_url": "cover_image_url",
                "sub_tilte": "sub_title",
                "introduction": "introduction",
                "contents": "content",
                "page": 1,
                "volume": 1,
                "date": "2020-01-01",
                "complete_time": "1시간 1분",
                "complete_per": 20,
                "publisher": "Publisher",
                "publisher_intro": "introduction",
                "author": ["Lee"],
                "category": "cate",
                "category_complete_time": "1시간 1분",
                "category_complete_per": 10,
                "comment_count": 1
            },
                "savebutton": True
        })

    def test_BookDetail_get_fail(self):
        client = Client()
        response = client.get('/book/id=1')
        self.assertEqual(response.status_code, 404)

    def test_BookDetail_get_not_exist_book(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.get('/book/9999', **{"HTTP_Authorization" : token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': 'NOT_EXIST_BOOK'})

class CategoryListTest(TestCase):

    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=12, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo' )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()

    def test_categorylist_get_success(self):
        client = Client()
        response = client.get('/book/category')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'categories': [{'category_id': 1, "image" : "cover_image_url", "name" : "cate" }]})

    def test_categorylist_get_fail(self):
        client = Client()
        response = client.get('/book/categories')
        self.assertEqual(response.status_code, 404)

class SubCategoryListTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=12, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo' )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()

    def test_subcategorylist_get_success(self):
        client = Client()
        response = client.get('/book/category/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'subcategories': [{
                'subcategory_id': 1,
                "subcategory_name" : "subcate",
                "books" : [{"book_id" : 1,"book_image" : 'small_image_url' }] }]})

    def test_subcategorylist_get_fail(self):
        client = Client()
        response = client.get('/book/category/900')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': 'NOT_EXIST_SUBCATEGORY'})

class BookSearchTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=12, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo' )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Author.objects.create(id=1, name='Kim')
        Author.objects.create(id=2, name='Lee')
        BookToAuthor.objects.create(id=1, book_id=1, author_id=2)

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        BookToAuthor.objects.all().delete()

    def test_booksearch_get_success(self):
        client = Client()
        response = client.get('/book/search/ti')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.json(), {'MESSAGE':[ {
            "book_id"    : 1,
            "book_title" : 'title',
            'book_image' : 'small_image_url',
            'author'     : ['Lee']
        }]})

    def test_booksearch_get_fail(self):
        client = Client()
        response = client.get('/book/search')
        self.assertEqual(response.status_code, 404)

    def test_booksearch_get_no_result(self):
        client = Client()
        response = client.get('/book/search/titles')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'MESSAGE': 'NO_RESULT'})

class CommentTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=12, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo1',profile_image_url="test1" )
        User.objects.create( id=11, name = 'hello3', usertype_id = 1, mobile = '01000040004',shelf_name='helloo2',profile_image_url="test2" )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Comment.objects.create(id=1, user_id=12, book_id =1, content='content')
        CommentLike.objects.create(id=1, user_id=12, comment_id =1)

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()

    def test_comment_post_success(self):
        client  = Client()
        comment = {
            'content' : "hello"
        }
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.post('/book/1/comment', json.dumps(comment), **{"HTTP_Authorization" : token}, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'MESSAGE': 3})

    def test_comment_post_fail(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.post('/book/1/comment', **{"HTTP_Authorization" : token}, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE': "KEY_ERROR:'content'"})

    def test_comment_post_long_content(self):
        client  = Client()
        comment = {
            'content' : "hellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohello"
        }
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.post('/book/1/comment', json.dumps(comment), **{"HTTP_Authorization" : token}, content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'MESSAGE': 'T00_LONG_CONTENT'})


    def test_comment_get_success(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.get('/book/1/comment', **{"HTTP_Authorization" : token})

        self.assertEqual(response.status_code, 200)

    def test_comment_get_fail(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.get('/book/9999/comment', **{"HTTP_Authorization" : token})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"MESSAGE": "NOT_EXIST_BOOK"})

    def test_comment_delete_success(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.delete('/book/1/comment?comment_id=1', **{"HTTP_Authorization" : token})

        self.assertEqual(response.status_code, 204)

    def test_comment_delete_fail(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.delete('/book/1/comment?comment_id=10', **{"HTTP_Authorization" : token})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"MESSAGE": "NOT_EXIST_COMMENT"})

    def test_comment_delete_except(self):
        client  = Client()
        token = jwt.encode({'user_id' :User.objects.get(id=11).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.delete('/book/1/comment?comment_id=1', **{"HTTP_Authorization" : token})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{"MESSAGE": "NOT_THIS_USER"})

class CommentLikeTest(TestCase):
    
    def setUp(self):
        Usertype.objects.create( id = 1, name = 'mobile' )
        User.objects.create( id=12, name = 'hello2', usertype_id = 1, mobile = '01000030003',shelf_name='helloo1',profile_image_url="test1" )
        User.objects.create( id=11, name = 'hello3', usertype_id = 1, mobile = '01000040004',shelf_name='helloo2',profile_image_url="test2" )
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='subcate',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Comment.objects.create(id=1, user_id=12, book_id =1, content='content1')
        Comment.objects.create(id=2, user_id=12, book_id =1, content='content2')
        CommentLike.objects.create(id=1, user_id=12, comment_id =1)

    def tearDown(self):
        User.objects.all().delete()
        Usertype.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Comment.objects.all().delete()
        CommentLike.objects.all().delete()

    def test_commentlike_patch_success(self):
        client  = Client()
        comment = {
            'comment_id' : 2
        }
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.patch('/book/commentlike', json.dumps(comment), **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS", "likebutton" : True })

    def test_commentlike_patch_cancel(self):
        client  = Client()
        comment = {
            'comment_id' : 1
        }
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.patch('/book/commentlike', json.dumps(comment), **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 204)

    def test_commentlike_patch_fail(self):
        client  = Client()
        comment = {
            'comment_id' : 5
        }
        token = jwt.encode({'user_id' :User.objects.get(id=12).id}, SECRET['secret'], algorithm = SECRET['algorithm']).decode('utf-8')
        response = client.patch('/book/commentlike', json.dumps(comment), **{"HTTP_Authorization" : token}, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "NOT_EXIST_COMMENT"})

class BookLikeTest(TestCase):
    
    def setUp(self):
        Publisher.objects.create( id=1, name='Publisher', introduction='introduction')
        Category.objects.create(id=1, name = "cate", complete_time='1:01', complete_percent =10)
        Subcategory.objects.create(id=1, name='베스트셀러',category_id =1)
        Book.objects.create( 
            id               = 1,
            title            = 'title',
            cover_image_url  = 'cover_image_url',
            small_image_url  = 'small_image_url',
            sub_title        = 'sub_title',
            introduction     = 'introduction',
            contents         = 'content',
            pages            = 1,
            volume           = 1,
            publication_date = '2020-01-01',
            complete_time    = '1:01',
            complete_percent = 20,
            subcategory_id   = 1,
            publisher_id     = 1
        )
        Author.objects.create(id=1, name='Kim')
        Author.objects.create(id=2, name='Lee')
        BookToAuthor.objects.create(id=1, book_id=1, author_id=2)

    def tearDown(self):
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        BookToAuthor.objects.all().delete()

    def test_booklist_get_success(self):
        client = Client()
        response = client.get('/book?limit=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"MESSAGE": [{
            "id" : 1,
            "book_img" : 'small_image_url',
            "book_name": "title",
            "book_author" : ["Lee"]
        }]})

    def test_booklist_get_fail(self):
        client = Client()
        response = client.get('/book/limit')
        self.assertEqual(response.status_code, 404)