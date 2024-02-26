from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .models import Post, PostLike, PostComment, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from shared.custom_pagination import CustomPagination
# Create your views here.

class PostListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response(
            {
                "success":True,
                "code":status.HTTP_200_OK,
                "message": "Post successfully update",
                "data": serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                "success":True,
                "code":status.HTTP_204_NO_CONTENT,
                "message": "Post successfully delete",
            }
        )


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset


class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id = post_id)


class PostLikeApiView(APIView):
    def post(self, request, pk):
        try:
            post_like = PostLike.objects.get(author=self.request.user, post_id=pk)
            post_like.delete()
            data = {
                "success":True,
                "message":"LIKE muvaffaqiyatli o'chirildi"
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist as e:
            post_like = PostLike.objects.create(author=self.request.user, post_id=pk)
            serializer = PostLikeSerializer(post_like)
            data = {
                "success":True,
                "message": "Postga LIKE muvaffaqiyatli qoshildi",
                "data":serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)


class CommentLikeAPIView(APIView):
    def post(self, request, pk):
        try:
            comment_like = CommentLike.objects.get(author=self.request.user, comment_id=pk)
            comment_like.delete()
            data = {
                "success":True,
                "message":"Comment LIKE ochirildi"
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist as e:
            comment_like = CommentLike.objects.create(author=self.request.user, comment_id=pk)
            serializer = CommentLikeSerializer(comment_like)
            data = {
                "success":True,
                "message":"Commentariga LIKE bosildi",
                "data":serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
