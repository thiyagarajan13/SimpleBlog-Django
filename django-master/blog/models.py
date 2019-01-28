from django.db import models
from django import forms 
# Create your models here.

from datetime import date
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #Blog author or commenter



class BlogAuthor(models.Model):
    """
    Model representing a blogger.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400, help_text="Enter your bio details here.")
    
    class Meta:
        ordering = ["user","bio"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog-author instance.
        """
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.username


class Blog(models.Model):
    """
    Model representing a blog post.
    """
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
      # Foreign Key used because Blog can only have one author/User, but bloggsers can have multiple blog posts.
    description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateField(default=date.today)
    blog_image = models.ImageField(upload_to='images/')
    likes = models.ManyToManyField(User, blank=True, related_name='blogpersonal_likes')
    class Meta:
        ordering = ["-post_date"]
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def __unicode__(self):
        """
        String for representing the Model object.
        """
        return self.name
        
    def  get_api_like_url(self):
        return reverse('like-api-toggle', kwargs={"pk":self.pk})
    
    def  get_like_url(self):
        return reverse('like-toggle', kwargs={"pk":self.pk})
        
class BlogComment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
      # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    blog= models.ForeignKey(Blog, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    class Meta:
        ordering = ["post_date"]
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title=75
        if len(self.description)>len_title:
            titlestring=self.description[:len_title] + '...'
        else:
            titlestring=self.description
        return titlestring
    def  get_likecomment_url(self):
        return reverse('likecomment-toggle',kwargs={'pk_1': self.id,'pk':self.blog_id})

    def  get_api_like_url(self):
        return reverse('likecomment-api-toggle',kwargs={'pk_1': self.id,'pk':self.blog_id})


