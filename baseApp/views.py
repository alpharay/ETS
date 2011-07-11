# Create your views here.
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from models import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
    t = loader.get_template('baseApp/index.html')
    c = Context(dict())
    return HttpResponse(t.render(c))
    
    
    
    
def categories_list(request, limit=100):
	blog_list = EventCategory.objects.all()
	t = loader.get_template('blog/list.html')
	c = Context({'blog_list':blog_list})
	return HttpResponse(t.render(c))

def events_list(request, limit=100):
	blog_list = Blog.objects.all()
	t = loader.get_template('blog/list.html')
	c = Context({'blog_list':blog_list})
	return HttpResponse(t.render(c))

class CommentForm(ModelForm):
	class Meta:
		model=Comment
		exclude=['post','author']
	
@csrf_exempt
def event_detail(request,id,showComments=False):
	single_blog = Blog.objects.get(id=id)
	print single_blog	
	if showComments:
		comment = Comment.objects.filter(post__id=id)
		print comment
		#Start of form code
		if request.method == 'POST':
			comment= Comment(post=single_blog,author=request.user.username)
			form = CommentForm(request.POST,instance=comment)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(request.path)
		else:
			form = CommentForm()
		#end of form code

	t = loader.get_template('blog/detail.html') # to detail.html
	c = Context({'comments':comment,'blog':single_blog,'form':form.as_p(),'username':request.user.username})
	return HttpResponse(t.render(c))


@csrf_exempt	
def edit_comment(request,id):
	comment = Comment.objects.get(pk=id)
	if request.user.username==comment.author:	
		if request.method == 'POST':			
			form = CommentForm(request.POST,instance=comment)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/blog/detail/'+str(comment.post.id)+'/True')
		else:
			form = CommentForm(instance=comment)
			t = loader.get_template('blog/editcomment.html') # to editcomment.html
			c = Context({'form':form.as_p()})
			return HttpResponse(t.render(c))
	return HttpResponse("You do not have enough permissions to edit this comment")
