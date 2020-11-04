from django.db   import models

class Library(models.Model):
    user       = models.ForeignKey("user.User", on_delete = models.CASCADE)
    book       = models.ForeignKey("book.Book", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    read       = models.BooleanField()

    class Meta:
        unique_together = ("user", "book")
        db_table = "libraries"

class Shelf(models.Model):
    user       = models.ForeignKey("user.User", on_delete = models.CASCADE)
    name       = models.CharField(max_length = 100)
    shelfbook  = models.ManyToManyField("book.Book", through = "ShelfToBook", related_name = "bookshelf")

    class Meta:
        db_table = "shelves"

class ShelfToBook(models.Model):
    book  = models.ForeignKey("book.Book", on_delete = models.CASCADE, related_name = "books")
    shelf = models.ForeignKey("Shelf", on_delete = models.CASCADE, related_name = "shelves")

    class Meta:
        unique_together = ("book", "shelf")
        db_table = "shelf_books"