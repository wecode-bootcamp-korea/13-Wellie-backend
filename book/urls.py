from django.urls import path
from book.views  import (
    BookDetailView,
    CategoryListView,
    SubCategoryListView,
    BookSearchView,
    CommentView,
    CommentLikeView,
    BooklistView
)

urlpatterns = [
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/category', CategoryListView.as_view()),
    path('/category/<int:category_id>', SubCategoryListView.as_view()),
    path('/search/<str:keyword>', BookSearchView.as_view()),
    path('/<int:book_id>/comment', CommentView.as_view()),
    path('/commentlike', CommentLikeView.as_view()),
    path('', BooklistView.as_view()),
]
