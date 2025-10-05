from rest_framework import viewsets, permissions, generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404 # get_object_or_404 불러오기
from .models import Book # 모델 불러오기
from .serializers import BookSerializer # 시리얼라이저 불러오기

@api_view(['GET'])
def helloAPI(request):
    return Response("hello world!")

# FBV(Function Based View, 함수 기반 뷰)
@api_view(['GET', 'POST']) # GET/POST 요청을 처리하게 만들어주는 데코레이터
def booksAPI(request): # /book/
    if request.method == 'GET': # GET 요청(도서 전체 정보)
         books = Book.objects.all() # Book 모델에서 전체 데이터 가져오기
         serializer = BookSerializer(books, many=True)
         # 시리얼라이저에 전체 데이터를 한 번에 집어넣기(직렬화, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST': # POST 요청(도서 정보 등록)
        serializer = BookSerializer(data=request.data)
        # POST 요청으로 들어온 데이터를 시리얼라이저에 집어넣기
        if serializer.is_valid(): # 유효한 데이터라면
            serializer.save()
            # 시리얼라이저의 역직렬화를 통해 save(), 모델시리얼라이저의 기본 create() 함수 동작
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def bookAPI(request, bid): # /book/bid/
    book = get_object_or_404(Book, bid=bid) # bid = id 인 데이터를 Book에서 가져오고, 없으면 404 에러
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

# CBV(Class Based View, 클래스 기반 뷰)
class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs): # GET 메소드 처리 함수(전체 목록)
        return self.list(request, *args, **kwargs) # mixins.ListModelMixin과 연결
    def post(self, request, *args, **kwargs): # POST 메소드 처리 함수(1권 등록)
        return self.create(request, *args, **kwargs) # mixins.CreateModelmixin과 연결

class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'
    # 우리는 Django 기본 모델 pk가 아닌 bid를 pk로 사용하고 있으니 lookup_field로 설정

    def get(self, request, *args, **kwargs): # GET 메소드 처리 함수(1권)
        return self.retrieve(request, *args, **kwargs) # mixins.RetrieveModelMixin과 연결
    def put(self, request, *args, **kwargs): # PUT 메소드 처리 함수(1권 수정)
        return self.update(request, *args, **kwargs) # mixins.UpdateModelMixin과 연결
    def delete(self, request, *args, **kwargs): # DELETE 메소드 처리 함수(1권 삭제)
        return self.destroy(request, *args, **kwargs) # mixins.DestroyModelMixin과 연결

class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

class BookViewSet(viewsets.ModelViewSet): # 라우터 지정 필요
    queryset = Book.objects.all()
    serializer_class = BookSerializer