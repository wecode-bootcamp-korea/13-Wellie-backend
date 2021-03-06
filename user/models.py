from django.db import models

class User(models.Model):
    social_id         = models.CharField(max_length = 100, null =True)
    name              = models.CharField(max_length = 50, unique=True)
    mobile            = models.CharField(max_length = 50, null =True)
    email             = models.CharField(max_length = 50, null =True)
    password          = models.CharField(max_length = 200, null =True)
    profile_image_url = models.URLField(max_length = 1000, null = True)
    library_image_url = models.URLField(max_length = 1000, null = True)
    created_at        = models.DateTimeField(auto_now_add = True)
    updated_at        = models.DateTimeField(auto_now = True)
    usertype          = models.ForeignKey("Usertype", on_delete = models.CASCADE)
    subscribe         = models.ManyToManyField("Subscribe", through = "UserToSubscribe", related_name = "subscriber")
    following         = models.ManyToManyField("self", symmetrical = False, through = "Follow", related_name = "followed")
    shelf_name        = models.CharField(max_length = 50)

    class Meta:
        db_table = "users"

class Usertype(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "usertypes"

class Subscribe(models.Model):
    name  = models.CharField(max_length = 50, unique=True)
    price = models.IntegerField(default = 0)

    class Meta:
        db_table = "subscribes"

class UserToSubscribe(models.Model):
    user         = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
    subscribe    = models.ForeignKey(Subscribe, on_delete = models.CASCADE, related_name = "subscribe")
    started_at   = models.DateField(auto_now_add = True)
    expirated_at = models.DateField(null=True)
    free         = models.BooleanField(default=False)
    number       = models.IntegerField(default = 0)

    class Meta:
        unique_together = ("user", "subscribe")
        db_table        = "users_subscribes"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "reader")
    reader   = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "follower")

    class Meta:
        unique_together = ("follower", "reader")
        db_table        = "follows"

class PhoneCheck(models.Model):
    check_id = models.CharField(max_length = 50)
    check_number = models.CharField(max_length = 20)

    class Meta:
        db_table        = "phonechecks"