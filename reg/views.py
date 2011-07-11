from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
	phone = forms.CharField()
	email = forms.EmailField()
    
@csrf_exempt
def loginView(request):
    if request.method == 'POST':
    #YOUR CODE HERE
        uname=request.POST['username']
        upass=request.POST['password']
        user=authenticate(username=uname,password=upass)
        if user is not None:
            if user.is_active:
                login(request,user)
                return render_to_response('baseApp/index.html')
            else:
                return HttpResponse('Your account has been disabled')
        else:
            log='invalid user name or password'
            form = LoginForm()
            return render_to_response('reg/login.html', {'form': form, 'logged_in': request.user.is_authenticated(),'log':log})

                       
    form = LoginForm()
    return render_to_response('reg/login.html', {'form': form, 'logged_in': request.user.is_authenticated()})

@csrf_exempt
def signupView(request):
	


@csrf_exempt
def logoutView(request):
    logout(request)
    return render_to_response('reg/logout.html')# Create your views here.
