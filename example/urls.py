from django.urls import path, include
from .views import helloAPI, booksAPI, bookAPI, BooksAPI, BookAPI

urlpatterns = [
    path('hello/', helloAPI),
    path('fbv/books/', booksAPI),
    path('fbv/book/<int:bid>/', bookAPI), # 함수형 뷰의 booksAPI 연결
    path('cbv/books/', BooksAPI.as_view()),
    path('cbv/book/<int:bid>/', BookAPI.as_view()), # 클래스형 뷰의 BooksAPI 연결
]