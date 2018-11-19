from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	request.session.clear()
	return render(request, "myapp/index.html")

def create(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.add_message(request, messages.ERROR, value, extra_tags='register')
		return redirect('/')
	else:
		password = request.POST['password']
		password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		User.objects.create(first_name= request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password= password)
		request.session['email'] = request.POST['email']
		request.session['user_id'] = User.objects.get(email= request.POST['email']).id 
	return redirect('/logged')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.add_message(request, messages.ERROR, value, extra_tags= "login")
		return redirect('/')
	else: 
		request.session['email'] = request.POST['email_log']
		request.session['user_id'] = User.objects.get(email= request.POST['email_log']).id 

	return redirect('/logged')

def logged(request):
	if 'user_id' not in request.session:
		return redirect('/')
		# this needs to be coded better
		#maybe try something like Review.objects.all().reverse()[0]
	elif int(Review.objects.last().id) >=3:
		reviewlast = Review.objects.last().id

		context = {
		"books" : Book.objects.all(),
		"review1": Review.objects.get(id = reviewlast),
		"review2": Review.objects.get(id = (reviewlast -1)),
		"review3": Review.objects.get(id = (reviewlast -2))
		}
		return render(request, 'myapp/logged.html', context)
	else:
		return render(request, 'myapp/logged.html') 


def review(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		context = {
		"books": Book.objects.all()
		}
		return render(request, 'myapp/review.html', context)

def addReview(request):

	Book.objects.create(title= request.POST['title'], author= request.POST['author'] , user_id= request.session['user_id'] )
	Review.objects.create(review= request.POST['review'], rating= request.POST['rating'], book_id= Book.objects.get(title= request.POST['title']).id, user_id= request.session['user_id'] )
	request.session['book_id'] = Book.objects.get(title= request.POST['title']).id
	bookid = str(request.session['book_id'])

	return redirect('bookprofile/' + bookid )

def addReview2(request):
	Review.objects.create(review= request.POST['review'], rating= request.POST['rating'], book_id= request.session["book_id"], user_id= request.session['user_id'] )
	return redirect('bookprofile/'+ str(request.session['book_id']))

def userProfile(request, userid): 
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		context = {
		"user" : User.objects.get(id = userid),
		"reviews" : Review.objects.filter(user_id = userid)
		}
		return render(request, 'myapp/user.html', context)

def bookProfile(request, bookid):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		context = {
		"book": Book.objects.get(id = bookid),
		"reviews": Review.objects.filter(book_id = bookid),
		"books": Book.objects.filter()
		}
		request.session['book_id'] = bookid 
		return render(request, 'myapp/book.html', context)

def delete(request, reviewid):
	Review.objects.get(id = reviewid).delete()
	return redirect('bookprofile/'+ str(request.session['book_id']))