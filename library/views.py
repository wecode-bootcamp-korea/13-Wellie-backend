import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Max
from django.db.models import Q

from user.utils       import login_decorator
from user.models      import User, Follow
from book.models      import Book
from library.models   import (
    Library,
    Shelf,
    ShelfToBook
)

class MyBookView(View) :

    @login_decorator
    def post(self, request) :
        try :
            user_id = request.user.id
            data    = json.loads(request.body)
            book_id = data["book_id"]
            if Book.objects.filter(id = book_id).exists() :
                library = Library.objects.get(user_id=user_id, book_id = book_id)
                library.delete()                
                return JsonResponse({"MESSAGE": "DELETE", "savebutton" : False }, status=201)
            else :
                return JsonResponse({"MESSAGE": "NOT_EXIST_BOOK"}, status=401)

        except Library.DoesNotExist :
            Library.objects.create(user_id=user_id, book_id = book_id)
            return JsonResponse({"MESSAGE": "SUCCESS", "savebutton" : True }, status=201)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

    @login_decorator
    def get(self, request) :
        user_id  = request.user.id
        sort     = request.GET.get('sort','register')
        readbook = request.GET.get('read')

        sort_dictionary = {
            'register'  : "created_at",
            'title'     : "bookName",
            'published' : "publication_date"
        }
        my_books = Book.objects.prefetch_related('author','library_set').filter(library__user_id=user_id)
        booklist = [ {
            "id"               : book.id ,
            "bookCoverImg"     : book.small_image_url,
            "bookName"         : book.title,
            "writer"           : [ authors.name for authors in book.author.all() ],
            "publication_date" : book.publication_date,
            "created_at"       : book.library_set.get(user_id=user_id).created_at,
            "read"             : book.library_set.get(user_id=user_id).read
        } for book in my_books ]
        if readbook :
            booklist = [ book for book in booklist if book["read"] ]
        booklist = sorted(booklist, key=lambda x: x[ sort_dictionary[sort] ])
        return JsonResponse({"bookCount": len(my_books), "books" : booklist }, status=200)

    @login_decorator
    def delete(self, request) :
        try :
            user_id          = request.user.id
            data             = json.loads(request.body)
            booklist_id_list = data["booklist"]
            my_books         = Library.objects.filter(user_id=user_id, book_id__in=booklist_id_list)
            my_books.delete()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=204)

        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except TypeError :
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class ShelfView(View) :
    
    @login_decorator
    def get(self, request) :
        user_id = request.user.id
        shelves = Shelf.objects.prefetch_related("shelfbook","shelfbook__book").filter(user_id = user_id).order_by('index')
        shelflist = [ {
            "id"             : shelf.id,
            "bookShelfName"  : shelf.name,
            "bookPreviewImg" : [ book.small_image_url for book in shelf.shelfbook.all()[0:2] ],
            "bookShelfIndex" : shelf.index
        } for shelf in shelves ]
        return JsonResponse({"bookShelfCount": len(shelves), "myBookShelfList" : shelflist }, status=200)

    @login_decorator
    def patch(self, request) :
        try :
            user_id       = request.user.id
            data          = json.loads(request.body)
            shelves_order = data["shelves"]

            for i in range(len(shelves_order)-1) :
                for j in range(i+1,len(shelves_order)):
                    if shelves_order[i][1] == shelves_order[j][1] :
                        return JsonResponse({"MESSAGE": "Invalid_INDEX"}, status=400)

            for i in shelves_order :
                shelf       = Shelf.objects.get(id=i[0], user_id = user_id)
                shelf.index = i[1]
                shelf.save()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except Shelf.DoesNotExist :
            return JsonResponse({'MESSAGE': "NOT_EXIST_SHELF" }, status=400)

    @login_decorator
    def delete(self, request) :
        try : 
            user_id  = request.user.id
            shelf_id = request.GET['shelf_id']
            shelf    = Shelf.objects.get(id=shelf_id, user_id = user_id)
            shelf.delete()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=204)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except Shelf.DoesNotExist :
            return JsonResponse({'MESSAGE': "NOT_EXIST_SHELF" }, status=400)


class ShelfDetailView(View) :
    
    @login_decorator
    def get(self, request) :
        try :
            user_id  = request.user.id
            shelf_id = request.GET['shelf_id']
            shelf    = Shelf.objects.get(id=shelf_id)
            booklist = [ {
                "id"           : book.id,
                "bookCoverImg" : book.small_image_url,
                "bookName"     : book.title,
                "writer"       : [ authors.name for authors in book.author.all() ]
            } for book in shelf.shelfbook.prefetch_related("author") ]
            return JsonResponse({"bookShelfName": shelf.name, "bookShelfCase" : booklist }, status=200)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except Shelf.DoesNotExist :
            return JsonResponse({'MESSAGE': "NOT_EXIST_SHELF" }, status=400)

    @login_decorator
    def patch(self, request) :
        try :
            user_id          = request.user.id
            data             = json.loads(request.body)
            shelf_id         = data["shelf_id"]
            shelfname        = data['shelfname']
            booklist_id_list = data["booklist"]

            shelf_book = ShelfToBook.objects.filter(shelf_id = shelf_id ).exclude(book_id__in = booklist_id_list )
            shelf_book.delete()
            
            shelf = Shelf.objects.get(id=shelf_id)
            shelf.name = shelfname
            shelf.save()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except Shelf.DoesNotExist :
            return JsonResponse({'MESSAGE': "NOT_EXIST_SHELF" }, status=400)

    @login_decorator
    def post(self, request) :
        try :
            user_id          = request.user.id 
            data             = json.loads(request.body)
            shelfname        = data['shelfname']
            booklist_id_list = data["booklist"]
            new_index = Shelf.objects.filter(user_id=user_id).aggregate(Max('index'))['index__max']
            if new_index :
                shelf     = Shelf.objects.create( user_id=user_id, name = shelfname, index = new_index +1 )
            else :
                shelf     = Shelf.objects.create( user_id=user_id, name = shelfname, index = 1 )
            for book_id in booklist_id_list :
                if not ShelfToBook.objects.filter( book_id = book_id, shelf_id = shelf.id).exists() :
                    ShelfToBook.objects.create( book_id = book_id, shelf_id = shelf.id)
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

class MyShelfView(View) :

    @login_decorator
    def get(self, request) :
        user    = request.user 
        myshelf = {
            "id"          : user.id,
            "myBooksName" : user.shelf_name,
            "userName"    : user.name,
            "profile"     : user.profile_image_url,
            "readBooks"   : Library.objects.filter(Q(user_id=user.id) & Q(read=True)).count(),
            "follower"    : user.followed.count(),
            "following"   : user.following.count()
        }
        return JsonResponse({'mybooksInfo': myshelf}, status=200)