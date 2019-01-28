from django.shortcuts import render, render_to_response
from django import forms
import json
from django.http import JsonResponse


# Create your views here.
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User #Blog author or commenter


def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(
        request,
        'index.html',
    )
    
def blog_upload_view(request): 
  
    if request.method == 'POST': 
        form = blogForm(request.POST, request.FILES) 
  
        if form.is_valid():  
            stock = form.save(commit=False)
            mname=BlogAuthor.objects.get(user=request.user)
            stock.author =mname
            stock.save()
            return redirect('success') 
    else: 
        form = blogForm() 
    return render(request, 'blog_upload.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfuly uploaded') 
    
class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """
    model = Blog
    paginate_by = 5

    
from django.shortcuts import get_object_or_404

class BlogListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name ='blog/blog_list_by_author.html'
    
    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(BlogAuthor, pk = id)
        return Blog.objects.filter(author=target_author)
        
    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context
    
    

class BlogDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Blog

    
class BloggerListView(generic.ListView):
    """
    Generic class-based view for a list of bloggers.
    """
    model = BlogAuthor
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login. 
    """
    model = BlogComment
    fields = ['description',]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})

# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'

def SignUp(request):
   form = UserCreationForm(request.POST)
   if form.is_valid():
       fname=form.cleaned_data['username']
       form.save()
       uname=User.objects.get(username=fname)
       BlogAuthor_instance = BlogAuthor.objects.create(user=uname)
       return redirect('login')
   else:
       return render(request, 'signup.html', {'form':   form})

class BloglikeToggle(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
     bid =self.kwargs.get("pk")
     print(bid)
     obj=get_object_or_404(Blog, id=bid)
     url_ = obj.get_absolute_url()
     user=self.request.user
     if user.is_authenticated:
         if user in obj.likes.all():
             obj.likes.remove(user)
         else:    
             obj.likes.add(user)
     return url_

class CommentlikeToggle(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
     bid =self.kwargs.get("pk")
     cid =self.kwargs.get("pk_1")
     print(bid)
     print(cid)
     objb = get_object_or_404(Blog,id=bid)
     obj=get_object_or_404(BlogComment, id=cid,blog_id=bid)
     url_ = objb.get_absolute_url()
     user=self.request.user
     if user.is_authenticated:
         if user in obj.likes.all():
             obj.likes.remove(user)
         else:    
             obj.likes.add(user)
     return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class BloglikeAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None,pk=None):
        bid =self.kwargs.get("pk")
        print(bid)
        obj=get_object_or_404(Blog, id=bid)
        url_ = obj.get_absolute_url()
        user=self.request.user
        updated = False
        liked = False
        counts =0
        if user.is_authenticated:
           if user in obj.likes.all():
               liked = False
               obj.likes.remove(user)
           else:    
               liked = True
               obj.likes.add(user)
           updated = True
           counts=obj.likes.count()
           data = {
           "updated": updated,
           "liked":   liked,
           "likescount": counts
              }
        return Response(data)

class CommentlikeAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None,pk=None,pk_1=None):
        bid =self.kwargs.get("pk")
        cid =self.kwargs.get("pk_1")
        obj=get_object_or_404(BlogComment, id=cid,blog_id=bid)
        user=self.request.user
        updated = False
        liked = False
        counts =0
        if user.is_authenticated:
           if user in obj.likes.all():
               liked = False
               obj.likes.remove(user)
           else:    
               liked = True
               obj.likes.add(user)
           updated = True
           counts=obj.likes.count()
           data = {
           "updated": updated,
           "liked":   liked,
           "likescount": counts
              }
        return Response(data)


