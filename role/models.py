# from django.db import models
# from django.contrib.auth.models import User
#
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser,PermissionsMixin
# )
#
#
# class UserProfileManager(BaseUserManager):
#     def create_user(self, email, name, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             name=name,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, name, password):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             name=name,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user
#
#
# class UserProfile(AbstractBaseUser,PermissionsMixin):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     name = models.CharField(u'姓名', max_length=32)
#     phone = models.CharField(u'座机', max_length=32,blank=True,null=True)
#     mobile = models.CharField(u'手机', max_length=32)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(
#         ('staff status'),
#         default=False,
#         help_text=('Designates whether the user can log into this admin site.'),
#     )
#
#     bind_hosts = models.ManyToManyField("BindHost",blank=True)
#     host_groups = models.ManyToManyField("BusinessUnit",blank=True)
#
#     objects = UserProfileManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name',]
#
#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email
#
#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email
#
#     def __str__(self):              # __unicode__ on Python 2
#         return self.name
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     class Meta:
#         verbose_name_plural = "用户表"
#
#
# class AdminInfo(models.Model):
#     """
#     管理员表
#     """
#     user_info = models.OneToOneField("UserProfile",on_delete=models.CASCADE)
#     # username = models.CharField(u'用户名', max_length=64)
#     # password = models.CharField(u'密码', max_length=64)
#
#     class Meta:
#         verbose_name_plural = "管理员表"
#
#     def __str__(self):
#         return self.user_info.name
#
#
# class UserGroup(models.Model):
#     """
#     用户组
#     """
#     name = models.CharField(max_length=32, unique=True)
#     users = models.ManyToManyField('UserProfile')
#
#     class Meta:
#         verbose_name_plural = "用户组表"
#
#     def __str__(self):
#         return self.name