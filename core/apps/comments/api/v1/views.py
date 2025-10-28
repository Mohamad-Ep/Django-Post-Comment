from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CommentBlogSerializer
from ...models import BlogComment

# _______________________________________________________


class CommentBlogListApiView(viewsets.ModelViewSet):
    """
    Getting and creating article comments with api
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentBlogSerializer
    queryset = BlogComment.objects.filter(is_active=True)


# _______________________________________________________
