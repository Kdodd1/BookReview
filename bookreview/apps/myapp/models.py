from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.db import models 
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		#first names
		if len(postData['first_name']) < 1:
			errors['first_name'] = "*Name field must be at least 2 characters long"
		elif not NAME_REGEX.match(postData['first_name']):
			errors['first_name'] = "*Name must not contain special characters or numbers"
		#last names
		if len(postData['last_name']) < 1:
			errors['last_name'] = "*Name field must be at least 2 characters long"
		elif not NAME_REGEX.match(postData['last_name']):
			errors['last_name'] = "*Name must not contain special characters or numbers"
		#Email
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "*Email must be in email format"
		elif User.objects.filter(email = postData['email']):
			errors['email'] = "*Email is already in the database"
		#Password
		if len(postData['password']) < 7:
			errors['password'] = "*Password must be atleast 8 character long"
		elif postData['password_confirmation'] != postData['password']:
			errors['password'] = "*Password and Password Confirmation fields do not match"

		return errors

	def login_validator(self, postData):
		errors = {}

		if User.objects.filter(email = postData['email_log']):
			user = User.objects.get(email = postData['email_log'])

		else: 
			errors['email_log'] = "*Email is not in the database"
			return errors

		if not bcrypt.checkpw(postData['password_log'].encode(), user.password.encode()):
			errors['password_log'] = "*Email and password do not match"

		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email= models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	# books : One to many (Book)
	# reviews : One to many (Review)

	objects = UserManager()

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, related_name="books")
	# reviews: One to many (Review)

class Review(models.Model):
	review = models.TextField()
	rating = models.IntegerField()
	user = models.ForeignKey(User, related_name = "reviews")
	book = models.ForeignKey(Book, related_name ="reviews")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)