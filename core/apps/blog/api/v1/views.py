from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from ...models import Article
from apps.accounts.models import Profile
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
# _______________________________________________________

class PostListApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["article_title","id"]
    ordering_fields = ["published_date"]
    
    def get_queryset(self):
        articles = Article.objects.filter(is_active=True)
        articles = self.filter_queryset(articles)
        return articles
    
    def get(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(data=ser_data.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data={"details":"The post was successfully created."},status=status.HTTP_201_CREATED)
# _______________________________________________________

class PostDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_details'

    def get_object(self):
        post = get_object_or_404(Article,slug=self.kwargs['slug'])
        return post
    
    def get(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_object())
        return Response(data=ser_data.data,status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_object(),data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data,status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        ser_data = self.get_serializer(instance=self.get_object(),data=request.data,partial=True)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data,status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
# _______________________________________________________