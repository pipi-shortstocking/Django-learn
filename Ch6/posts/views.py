from rest_framework import viewsets

from users.models import Profile
from .models import Post
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [CustomReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']: # DRF viewset에서 'list'는 전체 조회, 'retrieve'는 단일 조회
            return PostSerializer
        return PostCreateSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)