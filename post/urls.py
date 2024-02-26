from django.urls import path
from .views import  PostListApiView, PostCreateView, PostRetrieveUpdateDestroyView, \
    PostCommentListView, PostCommentCreateView, PostLikeApiView, CommentLikeAPIView
urlpatterns = [
    path("posts/", PostListApiView.as_view()),
    path('posts/create/', PostCreateView.as_view()),
    path("posts/<uuid:pk>/", PostRetrieveUpdateDestroyView.as_view()),
    path("posts/<uuid:pk>/comments/", PostCommentListView.as_view()),
    path("posts/<uuid:pk>/create-comment/", PostCommentCreateView.as_view()),
    path("posts/<uuid:pk>/like/", PostLikeApiView.as_view()),
    path("comment/<uuid:pk>/like/", CommentLikeAPIView.as_view()),
]