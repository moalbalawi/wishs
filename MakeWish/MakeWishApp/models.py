from __future__ import unicode_literals
from django.db import models
import re
import bcrypt


# PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']):
            errors['email'] = "Email already exist."
        if len(postData['first_name'])<2:
            errors['first_name']="First Name should be at least 2 charachters!"
        if len(postData['last_name'])<2:
            errors['last_name']="Last Name should be at least 2 charachters!"
        if len(postData['password'])<8:
            errors['password8']="Password should be at least 8 charachters!"
        if postData['password']!=postData['confirm_password']:
            errors['password']="Passwords don't match"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(postData['email']) < 8:
            errors['email'] = "Email should be at least 8 characters."
        elif not user:
            errors['email'] = "Username is not found."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors['password'] = "Incorrect password!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        return errors  

    def create_user(self, postData):
        create = {}
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        email_hash = bcrypt.hashpw(postData['email'].encode(), bcrypt.gensalt())
        self.create(first_name = postData['first_name'], last_name=postData['last_name'], email=postData['email'], email_hash=email_hash, password=pw_hash)
        return create

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors['item'] = "Item must be no fewer than 3 characters."
        if len(postData['desc']) < 3:
            errors['first_name'] = "Description must be no fewer than 3 characters."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_hash = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="wishes",on_delete=models.CASCADE)
    objects = WishManager()

class Granted_wish(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')
    user = models.ForeignKey(User, related_name="granted_wishes",on_delete=models.CASCADE)
    objects = WishManager()