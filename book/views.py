import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from user.utils       import login_decorator
from library.models   import Library
from book.models      import (
    Book,
    Publisher,
    Subcategory,
    Category,
    Author,
    Comment,
    CommentLike
)

class BookDetailView(View) :

    @login_decorator
    def get(self, request, book_id) :
        try :
            user_id    = request.user.id
            book       = Book.objects.select_related("publisher","subcategory__category").prefetch_related('author','comment_set').get(id = book_id)
            bookdetail = {
                'user_name'              : request.user.name,
                'book_id'                : book.id, 
                'title'                  : book.title,
                'image_url'              : book.cover_image_url,
                'sub_tilte'              : book.sub_title,
                'introduction'           : book.introduction,
                'contents'               : book.contents,
                'page'                   : book.pages,
                'volume'                 : book.volume,
                'date'                   : book.publication_date,
                'complete_time'          : f'{book.complete_time.hour}시간 {book.complete_time.minute}분',
                'complete_per'           : book.complete_percent,
                'publisher'              : book.publisher.name,
                'publisher_intro'        : book.publisher.introduction,
                'author'                 : [authors.name for authors in book.author.all()],
                'category'               : book.subcategory.category.name,
                'category_complete_time' : f'{book.subcategory.category.complete_time.hour}시간 {book.subcategory.category.complete_time.minute}분',
                'category_complete_per'  : book.subcategory.category.complete_percent,
                'comment_count'          : book.comment_set.count()
            }
            return JsonResponse({
                'MESSAGE'   : bookdetail,
                "savebutton": Library.objects.filter(user_id=user_id, book_id = book_id).exists()
            }, status=200)

        except Book.DoesNotExist : 
            return JsonResponse({'MESSAGE': 'NOT_EXIST_BOOK'}, status=400)

class CategoryListView(View) :

    def get(self, request) :
        categories   = Category.objects.prefetch_related('subcategory_set__book_set').all()
        categorylist = [ {
            "category_id" : category.id,
            "image"       : category.subcategory_set.all()[0].book_set.all()[0].cover_image_url,
            "name"        : category.name
        } for category in categories ]
        return JsonResponse({'categories': categorylist }, status=200)

class SubCategoryListView(View) :

    def get(self, request, category_id) :
        subcategories = Subcategory.objects.prefetch_related('book_set').filter(category_id = category_id)
        if subcategories :
            subcategorylist = [ {
                "subcategory_id"   : subcategory.id,
                "subcategory_name" : subcategory.name,
                "books"            : [ {
                    "book_id"    : book.id,
                    "book_image" : book.small_image_url
                } for book in subcategory.book_set.all() ]
            } for subcategory in subcategories ]
            return JsonResponse({'subcategories': subcategorylist }, status=200)
        return JsonResponse({'MESSAGE': 'NOT_EXIST_SUBCATEGORY'}, status=400)

class BookSearchView(View) :

    def get(self, request, keyword) :
        type   = request.GET.get('type','all')
        sort   = request.GET.get('sort','keyword')
        limit  = int(request.GET.get('limit','50'))
        offset = int(request.GET.get('offset','0'))

        type_filter = {
            'all'       : Q(author__name__icontains=keyword) | Q(title__icontains = keyword) | Q(publisher__name__icontains= keyword),
            'author'    : Q(author__name__icontains=keyword),
            'title'     : Q(title__icontains = keyword) ,
            'publisher' : Q(publisher__name__icontains= keyword)
        }

        sort_dic = {
            'keyword'   : 'id',
            'page'      : '-pages',
            'popular'   : '-complete_percent',
            'published' : 'publication_date'
        }

        books = Book.objects.prefetch_related('author').filter(type_filter[type]).order_by(sort_dic[sort]).distinct()[offset:offset+limit]
        if books :
            booklist = [ {
                "book_id"    : book.id,
                "book_title" : book.title,
                "book_image" : book.small_image_url,
                "author"     : [authors.name for authors in book.author.all()]                
            } for book in books ]
            return JsonResponse({'MESSAGE': booklist }, status=200)
        return JsonResponse({'MESSAGE': 'NO_RESULT'}, status=401)

class CommentView(View):

    @login_decorator
    def post(self, request, book_id) :
        if not Book.objects.filter(id = book_id).exists():
            return JsonResponse({"MESSAGE": "NOT_EXIST_BOOK"}, status=400)
        try :
            user_id = request.user.id
            data    = json.loads(request.body)
            content = data['content']
            if len(content) < 200 :
                comment = Comment.objects.create(
                    book_id = book_id,
                    user_id = user_id,
                    content = content
                )
                return JsonResponse({'MESSAGE': comment.id }, status=200)
            return JsonResponse({'MESSAGE': 'T00_LONG_CONTENT'}, status=401)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        except json.JSONDecodeError as e :
            return JsonResponse({'MESSAGE': f'Json_ERROR:{e}'}, status=400)

    @login_decorator
    def get(self, request, book_id) :            
        try :
            user_id     = request.user.id
            comments    = Book.objects.get(id=book_id).comment_set.all()
            commentlist = [ {
                "comment_id"   : comment.id,
                "user_name"    : comment.user.name,
                "user_img"     : comment.user.profile_image_url,
                "user_comment" : comment.content,
                "date"         : comment.created_at.strftime("%Y.%m.%d"),
                "likebutton"   : CommentLike.objects.filter(user_id=user_id, comment_id=comment.id).exists()    
            } for comment in comments ]
            return JsonResponse({"COMMENT": commentlist,"NAME": request.user.name }, status=200)

        except Book.DoesNotExist:
            return JsonResponse({"MESSAGE": "NOT_EXIST_BOOK"}, status=400)

    @login_decorator
    def delete(self, request, book_id) :            
        try :
            user_id    = request.user.id
            comment_id = request.GET["comment_id"]
            comment    = Comment.objects.get(id = comment_id)
            if comment.user_id == user_id :
                comment.delete()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=204)
            return JsonResponse({"MESSAGE": "NOT_THIS_USER" }, status=401)

        except Comment.DoesNotExist :
            return JsonResponse({"MESSAGE": "NOT_EXIST_COMMENT"}, status=400)
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)

class CommentLikeView(View):

    @login_decorator
    def patch(self, request) :
        try :
            user_id = request.user.id
            data    = json.loads(request.body)
            comment = data["comment_id"]
            if Comment.objects.filter(id = comment).exists() :
                like = CommentLike.objects.get(user_id=user_id, comment_id = comment)
                like.delete()
                return JsonResponse({"MESSAGE": "CANCEL", "likebutton" : False }, status=204)
            return JsonResponse({"MESSAGE": "NOT_EXIST_COMMENT"}, status=400)

        except CommentLike.DoesNotExist :
            CommentLike.objects.create(user_id=user_id, comment_id = comment)
            return JsonResponse({"MESSAGE": "SUCCESS", "likebutton" : True }, status=201)

class BooklistView(View) :
    
    def get(self, request) :
        limit  = int(request.GET.get('limit','10'))            
        books    = Book.objects.prefetch_related('author').filter(subcategory_id__in = [ subcategory.id for subcategory in Subcategory.objects.filter(name__icontains='베스트셀러') ] )[0:limit]
        booklist = [ {
            "id"          : book.id,
            "book_img"    : book.small_image_url,
            "book_name"   : book.title,
            "book_author" : [authors.name for authors in book.author.all()]
        } for book in books ]
        return JsonResponse({"MESSAGE": booklist }, status=200)