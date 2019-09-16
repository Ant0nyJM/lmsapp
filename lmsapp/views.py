from django.http import HttpResponse,JsonResponse,Http404
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from django.core import serializers

from django.contrib.auth.models import User
from lmsapp.models import Book
from lmsapp.forms import BookForm

import json

# Create your views here.

def userlogout(request):
    logout(request)
    return redirect('login')

def user_home(request,user_id):
    user = User.objects.get(pk=user_id)
    print("----------------------------------    " ,user.id)
    return render(request,'lmsapp/userhome.html',{'user':user})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("hello1")
            form.save()
            return redirect('login')
    else:
        print("hello2")
        form = UserCreationForm()
    return render(request,'lmsapp/signup.html',{'form':form})

def userlogin(request):
    if request.method == 'POST':
        print("values -->",request.POST)
        # form = AuthenticationForm(request.POST)
        # if form.is_valid():

        #     username = request.POST['username']
        #     user = authenticate(username= username,password=request.POST['password'])
        #     if(user is not None):
        #         login(request, user)
        #         if(user.has_perm('lmsapp.can_change')):
        #             return redirect('dash_book_issue')
        #         else:
        #             return redirect(reverse("user_home", args=[user.id]))
        #     else:
        #         return HttpResponse('Login Unsuccessfull')



        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username= username,password=password)
        if (user is not None):
            login(request, user)
            if(user.has_perm('lmsapp.can_change')):
                return redirect('dash_book_issue')
            else:
                return redirect(reverse("user_home", args=[user.id]))
        else:
            messages.error(request,'username or password not correct')
            return redirect('login')
    else:
        form = AuthenticationForm()
        print('------------- returning new form -----------')
        return render(request,'lmsapp/login.html',{'form':form})

##user search
def user_search(request):
    if request.method == 'POST':
        users = User.objects.filter(username__contains=request.POST['query'])
        if(len(users)==0):
            return HttpResponse('<p>No users found</p>')
        else:
            return render(request,'lmsapp/users_list.html',{'users':users})
    else:
        return HttpResponse("<h1>Not Allowed</h1>")

## book search page
def book_search(request):
    if request.method == 'POST':
        print(request.POST)
        query = request.POST['searchquery']
        #db_response = serializers.serialize('json',Book.objects.filter(book_name__contains=query))
        if(request.POST['searchparam'] == 'book_author'):
            db_response = Book.objects.filter(book_author__contains=query)

        else:

            db_response = Book.objects.filter(book_name__contains=query)


        #return JsonResponse({'results':db_response})
        return render(request,'lmsapp/booksearchresults.html',{'results':db_response})
    else:
        return render(request,'lmsapp/booksearch.html')

def get_book(request,book_id):
    try:
        details = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    request.session['current_view_book']=book_id
    return render(request,'lmsapp/getbook.html',{'book':details})

def dash_book_issue(request):
    if request.method == 'POST':
        book = Book.objects.get(book_id=request.session['current_view_book'])
        if(book.book_issued == False):
            u = User.objects.get(username=request.POST['username'])
            book.book_issuer = u
            book.book_issued = True
            book.save()
            print('Book id ------>',book.book_id)
            return JsonResponse({'msg':'Book Issued Successfully'})
    else:
        return render(request,'lmsapp/dash_book_issue.html')


def get_user(request,username):
    return render(request,'lmsapp/getuser.html',{'user':User.objects.get(username=username)})


def book_return(request):
    book = Book.objects.get(book_id=request.session['current_view_book'])
    book.book_issued = False
    book.book_issuer = None
    book.save()
    return JsonResponse({'msg':'Book returned'})

def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if(form.is_valid()):
            obj = form.save()
            return redirect(reverse('getbook',args=[obj.book_id]))
        else:
            return HttpResponse("Invalid submission")
    else:
        form = BookForm()
        return render(request,'lmsapp/book_add.html',{'form':form})


def passw_change(request,user_id):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return userlogout(request)
        else:
            return HttpResponse("Invalid form")
    else:
        form = PasswordChangeForm(request.user)
        return render(request,'lmsapp/passwchange.html',{'form':form})


def book_edit(request):
    book = Book.objects.get(book_id=request.session['current_view_book'])
    if(request.method == 'POST'):
        form = BookForm(request.POST,instance=book)
        if(form.is_valid()):
            form.save()
            return redirect(reverse('getbook',args=[book.book_id]))
    else:
        form = BookForm(instance=book)
        return render(request,'lmsapp/bookedit.html',{'form':form})

def book_delete(request):
    book = Book.objects.get(book_id=request.session['current_view_book'])
    if(book.book_issued):
        return JsonResponse({'ret-msg':'Book can only be deleted after return','deleted':'false'})
    else:
        book.delete()
        return JsonResponse({'ret-msg':'Book Successfully deleted','deleted':'true'})

