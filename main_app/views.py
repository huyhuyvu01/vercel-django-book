from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from users.models import CustomUser
from .models import Books, Ratings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .DataHandle.AllBookRecommend import GetBestStarBooks, GetData2Recommend, NameOfBookByUnratedUser, NameOfBookByUser, loadData, recommend
import datetime

# Create your views here.
def hello(request):
    return HttpResponse("Hello world!")

@login_required(login_url='login')
def HomePage(request):

    """Fixing"""
    try:
        # username with rated from 7 - 8 stars
        UserIdNow = request.user.id
        GetFinalName = NameOfBookByUser(UserIdNow)
        name = GetFinalName[0]["title"]
    except:
        name = NameOfBookByUnratedUser()

    BookObj, pt, similarity_score = GetData2Recommend()
    BookListForUserRecommend = recommend(BookObj, pt, similarity_score,name)
    BookListLovedByUser = GetBestStarBooks(BookObj)


    return render(request, 'index.html', {'BookList':BookListForUserRecommend, 'BookListLoved': BookListLovedByUser})

    # """Đc chạy cái này"""
    # BookObj, pt, similarity_score = GetData2Recommend()
    # BookList = recommend(BookObj, pt, similarity_score)
    # #booklist = Books.objects.all()
    # return render(request, 'index.html', {'BookList':BookList})


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Passwords do not match")
        else:
            my_user = CustomUser.objects.create_user(uname, pass1)
            my_user.save()
            print(uname, pass1, pass2)
            return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:    
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def AllBooks(request):
    booklist = loadData()

    p = Paginator(booklist, 9)

    pagenum = request.GET.get('pagenum', 1)

    try:
        page = p.page(pagenum)
    except EmptyPage:
        page = p.page(1)

    context = {'books': page}
    return render(request, 'all_books.html', context)

def DetailPage(request, ISBN):
    # book = get_object_or_404(Books, pk=ISBN)
    book = Books.objects.get(ISBN = ISBN)
    print(book.author)
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        user_id = request.user.id
        
        obj = Ratings.objects.update_or_create(user_id=user_id, ISBN=el_id, defaults={'rating':val})

        return JsonResponse({"Success":"true", "score":val}, safe=False)
    return render(request, 'detail.html', {'book': book})

def RateBook(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        user_id = request.user.id
        
        obj = Ratings.objects.filter(user_id=user_id, ISBN=el_id)
        if obj:
            obj.rating = val
            obj.save()
        else:
            rate = Ratings(user_id=user_id, ISBN=el_id, rating=val)
            rate.save()
        

        return JsonResponse({"Success":"true", 'score':'val'}, safe=False)
    return JsonResponse({"Success":'false'})

def AuthorPage(request):
    return render(request, 'author.html')

def RecommendPage(request):
    return render(request, 'recommend.html')