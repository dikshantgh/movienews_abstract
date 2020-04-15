from django.contrib.auth.models import User, PermissionsMixin, AbstractUser
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
import uuid

from taggit.managers import TaggableManager

from core.validators import phone_number_validator

"""
There are two ways of extending/substituting the default User model in django.
1. Create a new model for example People() and add all the non auth fields which are not required during authentication.
using OneToOneField() with User or use proxy
2. Substituting the User model by using AbstractBaseUser

Note: 
AbstractBaseUser : AbstractBaseUser only contains the authentication functionality, but no actual fields: 
you have to supply them when you subclass.
AbstractUser :AbstractUser is a full User model, complete with fields, as an abstract class so that you can inherit from
 it and add your own profile fields and methods. 
"""

# 1. create a new model with one to one field


# class People(models.Model):
#     user_person = models.OneToOneField(User, on_delete=models.CASCADE, related_name='people_name')
#     dob = models.DateField(verbose_name='Date of Birth', help_text="Format :'YYYY-MM-DD'", blank=True)
#     country = models.CharField(max_length=20, blank=True)
#     favourite_actor = models.CharField(max_length=20, blank=True)
#
#     def __str__(self):
#         return self.user_person.username
#
#     def get_absolute_url(self):
#         return reverse('core:profile_show', args=[self.pk, ])
#
#     class Meta:
#         verbose_name_plural = 'People'


# 2. Substituting the user model using AbstractUser(I am ok with username and email.) just add few new fields./ Or
# Creating a complete new slate for django AbstractBaseUser


# # incase of only abstractuser
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
# class User(AbstractUser):
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)



class Creator(AbstractUser):
    GENDER_CHOICES =(
        ('male', 'Male'),
        ('female', 'Female'),
        ('secret', 'Secret'),
    )
    # email = models.EmailField(verbose_name='Email', max_length=50, unique=True)
    # username = models.CharField(max_length=50, unique=True)
    # date_joined = models.DateTimeField(auto_now_add=True)
    # last_login = models.DateTimeField(auto_now=True)
    # is_admin = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # first_name = models.CharField(max_length=40, blank=True)
    # last_name = models.CharField(max_length=40, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dob = models.DateField(verbose_name='Date of birth', help_text='Format: YYYY-MM-DD', default=timezone.now)
    bio = models.TextField(max_length=1000, blank=True)
    country = models.CharField(max_length=15, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default='Unspecified', )
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='default_image.jpg')
    phone_number = models.CharField(max_length=10, help_text='Enter only numeric values of 10 digits', validators=[phone_number_validator, ])
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    # email_address = models.EmailField(max_length=50,)

    # USERNAME_FIELD = 'email'  # used as username field when log in or create user
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob', 'gender', 'phone_number', 'email', ]  # when registering. can also add first_name if wanted

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('core:profile_show', args=[self.id])

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    """
    I can use permissionmixin instead of these
    """
    # def has_perm(self, perm, obj=None):     # user can do stuffs if they are admin
    #     return self.is_admin
    #
    # def has_module_perms(self, app_label):
    #     return True


class PostManager(models.Manager):
    def get_trending(self):
        return self.filter(category='trending')


class Post(models.Model):
    POST_CATEGORY= (
        ('featured', 'Featured'),
        ('side_story', 'Side Story'),
        ('trending', 'Trending'),
        ('bin', 'bin'),
    )
    title = models.CharField(max_length=100,)
    author = models.ForeignKey(Creator, on_delete=models.DO_NOTHING, related_name='posts', )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = TaggableManager()
    view = models.PositiveIntegerField(default=0)
    picture = models.ImageField(upload_to='post/', null=True)
    category = models.CharField(max_length=50, choices=POST_CATEGORY, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:post_detail', kwargs={'slug': self.slug, })

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title, allow_unicode=True)
    #     return super(Post, self).save(*args, **kwargs)


