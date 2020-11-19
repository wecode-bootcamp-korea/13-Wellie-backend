from django.urls import path
from library.views  import (
    MyBookView,
    ShelfView,
    ShelfDetailView,
    MyShelfView
)

urlpatterns = [
    path('/mybook', MyBookView.as_view()),
    path('/shelf', ShelfView.as_view()),
    path('/shelfdetail', ShelfDetailView.as_view()),
    path('', MyShelfView.as_view()),
]