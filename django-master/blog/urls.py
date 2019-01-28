from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogger/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog_comment'),
    path('blog_upload',views.blog_upload_view, name = 'blog_upload'), 
    path('success', views.success, name = 'success'),
    path('signup/', views.SignUp, name='signup'),
    # url(r'^blog/(?P<id>\d+)/like$', views.BloglikeToggle.as_view, name='like-toggle'), #like feature
    path('blog/<int:pk>/like/', views.BloglikeToggle.as_view(), name='like-toggle'),
    path('blog/<int:pk>/clike/<int:pk_1>', views.CommentlikeToggle.as_view(), name='likecomment-toggle'),
    path('api/blog/<int:pk>/like/', views.BloglikeAPIToggle.as_view(), name='like-api-toggle'),
    path('api/blog/<int:pk>/clike/<int:pk_1>', views.CommentlikeAPIToggle.as_view(), name='likecomment-api-toggle'),
]



