from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from User import models
from django.contrib.auth.decorators import login_required
# Create your views here.
#from django.shortcuts import render_to_response
#from django.contrib.auth import authenticate, login

def login(request):
    c = {}
    c.update(csrf(request))

    return render_to_response('login.html',c)

def auth_view(request):
#    print "dasd"

    username = request.POST.get('username','')

    password = request.POST.get('pwd','')
    user = auth.authenticate(username=username,password=password)

    print user
    if user is not None:
            request.session['m_id'] = user.id
        #if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid/')
def loggedin(request):
    return render_to_response('loggedin.html',
                                   {'full_name': request.user.first_name})



def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    #print "yoyo"
    return HttpResponseRedirect('/accounts/login')
    #return render_to_response('logout.html')
"""def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")"""
def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return  render_to_response('sucess.html')
    else:
        form = UserCreateForm()
    return render(request, "signup.html", {
        'form': form,
    })


class UserCreateForm(UserCreationForm):


   # def save(self):
    #    user = models.User()

     #   user.save()
      #  return user


    class Meta:
        model = models.User
        fields = ('email','first_name','last_name','password1','password2')