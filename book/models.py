from django.db   import models

class Book(models.Model):
    title               = models.CharField(max_length = 100)
    cover_image_url     = models.URLField(max_length = 1000)
    sub_title           = models.CharField(max_length = 100, null = True)
    subcategory         = models.ForeignKey("Subcategory", on_delete = models.CASCADE)
    introduction        = models.CharField(max_length = 2000)
    author_introduction = models.CharField(max_length = 2000, null = True)
    contents            = models.CharField(max_length = 2000, null = True)
    pages               = models.IntegerField(default = 0)
    volume              = models.IntegerField(default = 0)
    publication_date    = models.DateField()
    complete_time       = models.TimeField(null = True)
    publisher           = models.ForeignKey("Publisher", on_delete = models.CASCADE)
    tags                = models.ManyToManyField("Tag", through = "BookToTag", related_name = "books_tags")

    class Meta:
        db_table = "books"

class Comment(models.Model):
    user       = models.ForeignKey("user.User", on_delete = models.CASCADE)
    book       = models.ForeignKey("Book", on_delete = models.CASCADE)
    content    = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "comments"

class CommentLike(models.Model):
    user    = models.ForeignKey("user.User", on_delete = models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete = models.CASCADE)

    class Meta:
        unique_together = ("user", "comment")
        db_table        = "comment_likes"

class Publisher(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        db_table = "publishers"

class Author(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "authors"

class BookToAuthor(models.Model):
    book   = models.ForeignKey("Book", on_delete = models.CASCADE)
    author = models.ForeignKey("Author", on_delete = models.CASCADE)

    class Meta:
        unique_together = ("book", "author")
        db_table = "books_authors"

class Category(models.Model):
    name             = models.CharField(max_length = 50)
    complete_time    = models.TimeField()
    complete_percent = models.IntegerField(null = True)

    class Meta:
        db_table = "categories"

class Subcategory(models.Model):
    name     = models.CharField(max_length = 50)
    category = models.ForeignKey("Category", on_delete = models.CASCADE)

    class Meta:
        db_table = "subcategories"

class Tag(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "tags"

class BookToTag(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = "book")
    tag  = models.ForeignKey(Tag, on_delete = models.CASCADE, related_name = "tag")

    class Meta:
        unique_together = ("book", "tag")
        db_table        = "books_tags"