from django.db import models
from Django_LoginSystem import settings
import random
import sys
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, userID, username, date_of_birth, email, profile_pic, password=None):
        if not username:
            raise ValueError('Usersmust have an email address')

        user = self.model(
            userID = random.randint(0, 999999),
            username = username,
            date_of_birth=date_of_birth,
            email=email,
            profile_pic=profile_pic
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, userID, username, date_of_birth, email, profile_pic, password=None):
        user = self.create_user(
            userID=random.randint(0, 999999),
            username=username,
            date_of_birth=date_of_birth,
            email=email,
            profile_pic=profile_pic,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def update_user(self, userID, username, date_of_birth, email, profile_pic, password):
        user = self.update(
            userID = userID,
            username = username,
            date_of_birth = date_of_birth,
            email = email,
            profile_pic = profile_pic,
        )
        user.set_password(password)
        return user

class User(AbstractBaseUser):
    userID = models.IntegerField(null=False, blank=False, primary_key=True)
    username = models.CharField(max_length=200, default=False, unique=True)
    date_of_birth = models.DateField(default=False)
    email = models.EmailField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    profile_pic = models.ImageField(verbose_name='profile_pic', upload_to='profile_pic/', null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'email', 'profile_pic', 'userID']

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_admin

    def get_id(self):
        return self.id

class Blogs(models.Model):
    thumbnail = models.ImageField(verbose_name='thumnbail', upload_to='Blog_Thumbnails', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    blog = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return 
    
    def get_id(self):
        return self.id
    
    def is_valid(self):
        return self.is_valid

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, default=None)
    comment = models.TextField(blank=False, null=False)
    blogName = models.ForeignKey(Blogs, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def is_valid(self):
        return self.is_valid