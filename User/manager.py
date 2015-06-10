#-*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.utils.crypto import get_random_string


class CustomUserManager(UserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        u = self.create_user(kwargs['email'], password=kwargs['password'])
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        u.is_staff = True
=======
        u.is_admin = True
>>>>>>> 2ed739edfd5f81fb5d365d4737e03de3c220daeb
=======
        u.is_admin = True
>>>>>>> 2ed739edfd5f81fb5d365d4737e03de3c220daeb
=======
        u.is_admin = True
>>>>>>> 2ed739edfd5f81fb5d365d4737e03de3c220daeb
        u.save(using=self._db)
        return u

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_unconfirmed_user(self, email=None, password=None, account_type=None, **extra_fields):
        """
        :rtype: profiles.models.User
        """
        if password is None:
            password = make_password(None)
        return super(CustomUserManager, self).create_user(
            email, password, account_type=account_type,
            is_active=False, **extra_fields
        )

    def generate_random_username(self):
        """
        Usernames that start with '!' are generated randomly and
        cannot be used for login until changed by the user.
        """
        return "!{}".format(get_random_string(length=16))