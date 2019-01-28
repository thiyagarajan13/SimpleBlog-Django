
# forms.py 
from django import forms 
from .models import *

class blogForm(forms.ModelForm): 
	class Meta: 
		model = Blog 
		fields = ['name','post_date', 'blog_image','description']
