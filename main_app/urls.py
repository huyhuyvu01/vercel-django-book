from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('books/', views.AllBooks, name='books'),
    path('books/<str:ISBN>/', views.DetailPage, name='detail'),
    path('books/<str:ISBN>/rate-book/', views.DetailPage, name='rate'),
    path('author/', views.AuthorPage, name='author'),
    path('recommend/', views.RecommendPage, name='recommend'),
]
