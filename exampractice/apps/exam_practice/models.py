from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
# Create your models here.



class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(username = post['username'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(),user.password.encode()) == user.password:

                return user

        return None




    def register(self,post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(),bcrypt.gensalt())
        User.objects.create(name=post['name'],username=post['username'],password=encrypted_password)




    def validate(self,post):
        errors = []

        if len(post['name']) == 0:
            errors.append('Name is required')

        if len(post['username']) == 0:
            errors.append('Username is required')

        if len(post['password']) == 0:
            errors.append('Password is required')

        elif len(post['password']) < 8:
            errors.append('Password must be at least 8 characters')

        elif post['password'] != post['pass_conf']:
            errors.append('Passwords must match')

        if len(User.objects.filter(username = post['username'])) > 0:
            errors.append('Username is unavailable')

        return errors



class User(models.Model):
    name = models.CharField(max_length=45)
    username=models.CharField(max_length=45)
    password= models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add= True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= UserManager()
