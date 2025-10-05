from django.urls import path, include
from .views import BookAPIGenerics, helloAPI, booksAPI, bookAPI, BooksAPI, BookAPI,BooksAPIMixins, BookAPIMixins, BooksAPIGenerics, BookAPIGenerics, BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books', BookViewSet)

urlpatterns = [
    path('hello/', helloAPI),
    path('fbv/books/', booksAPI),
    path('fbv/book/<int:bid>/', bookAPI), # 함수형 뷰의 booksAPI 연결
    path('cbv/books/', BooksAPI.as_view()),
    path('cbv/book/<int:bid>/', BookAPI.as_view()), # 클래스형 뷰의 BooksAPI 연결
    path('mixin/books/', BooksAPIMixins.as_view()),
    path('mixin/book/<int:bid>/', BookAPIMixins.as_view()),
    path('generics/books/', BooksAPIGenerics.as_view()),
    path('generics/book/<int:bid>/', BookAPIGenerics.as_view()),
    path('viewset/', include(router.urls)),
]