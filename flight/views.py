from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from flight.models import *
from django.views.decorators.csrf import csrf_exempt #include this 
import random
def welcome(request):
    template=loader.get_template("welcome.html")
    res=template.render()
    return HttpResponse(res)

def signup(request):
    template=loader.get_template("signup.html")
    res=template.render()
    return HttpResponse(res)

@csrf_exempt # include  this
def store_user(request):
    if request.method=='POST':
        username=request.POST['username']
        if(len(User.objects.filter(username=username))):
            msg='username already taken ....try another username'
            context={
                'msg':msg
            }
            template=loader.get_template("signup.html")
            res=template.render(context,request)
            return HttpResponse(res)
        else:
            user=User()
            user.username=username
            user.password=request.POST['password']
            user.name=request.POST['name']
            user.save()
            template=loader.get_template("store_user.html")
            res=template.render()
            return HttpResponse(res)
    else:
        msg='invalid request......first signup'
        context={
            'msg':msg
        }
        template=loader.get_template("signup.html")
        res=template.render(context,request)
        return HttpResponse(res)
    
@csrf_exempt # include  this
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if(len(User.objects.filter(username=username))):
            user=User.objects.filter(username=username)
            if(len(user.filter(password=password))):
                request.session['username']=username # login success then ...
                user_data=User.objects.filter(username=username)
                profile_data=Profile.objects.filter(username=username)
                context={
                    'user_data':user_data,
                    'profile_data':profile_data
                }
                template=loader.get_template("homepage.html")
                res=template.render(context,request)
                return HttpResponse(res)
            else:
                msg='incorrect password.......login again'
                context={
                    'msg':msg
                }
                template=loader.get_template("login.html")
                res=template.render(context,request)
                return HttpResponse(res)
        else:
            msg='incorrect username........login again'
            context={
                'msg':msg
            }
            template=loader.get_template("login.html")
            res=template.render(context,request)
            return HttpResponse(res)
    else:
        template=loader.get_template("login.html")
        res=template.render()
        return HttpResponse(res)

def homepage(request):
    if 'username' not in request.session.keys(): # session dict with key and value
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    else:
        username=request.session['username']
        user_data=User.objects.filter(username=username)
        profile_data=Profile.objects.filter(username=username)
        context={
            'user_data':user_data,
            'profile_data':profile_data
        }
        template=loader.get_template("homepage.html")
        res=template.render(context,request)
        return HttpResponse(res)
    
def profile(request):
    if 'username' not in request.session.keys(): # session dict with key and value
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    else:
        template=loader.get_template("profile.html")
        res=template.render()
        return HttpResponse(res)

@csrf_exempt # include  this
def profile_save(request):
    if request.method=='POST':
        username=request.session['username']
        profile=Profile()
        profile.username=User.objects.get(username=username)
        profile.fathers_name=request.POST['fathers_name']
        profile.mothers_name=request.POST['mothers_name']
        profile.email=request.POST['email']
        profile.phone=request.POST['phone']
        profile.save()
        username=request.session['username']
        user_data=User.objects.filter(username=username)
        profile_data=Profile.objects.filter(username=username)
        context={
            'user_data':user_data,
            'profile_data':profile_data
        }
        template=loader.get_template("homepage.html")
        res=template.render(context,request)
        return HttpResponse(res)
    else:
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)

def booking(request):
    if 'username' not in request.session.keys():
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    else:
        template=loader.get_template("booking.html")
        res=template.render()
        return HttpResponse(res)

@csrf_exempt # include  this
def result(request):
    if 'username' not in request.session.keys():
        template=loader.get_template("welcome.html")
        res=template.render()
        return HttpResponse(res)
    else:
        from_from=request.POST['from_from']
        to_to=request.POST['to_to']
        date=request.POST['date']
        request.session['flight_class']=request.POST['flight_class'] 
        request.session['count']=request.POST['count']
        flight=flights_from_to.objects.filter(from_from=from_from)
        flight=flight.filter(to_to=to_to)
        flight=flight.filter(date=date)
        if(len(flight)==0):
            template=loader.get_template("no_flight.html")
            res=template.render()
            return HttpResponse(res)
        context={
            'flight':flight,
            'from_from':from_from,
            'to_to':to_to
        }
        template=loader.get_template("result.html")
        res=template.render(context,request)
        return HttpResponse(res)

@csrf_exempt # include  this
def result2(request):
    if request.method=='POST':
        flight=request.POST['flight']
        flight_class=request.session['flight_class']
        count=request.session['count']
        base_price=fare.objects.filter(flight=flight)
        base_price=base_price.filter(flight_class=flight_class)
        for ele in base_price:
            base_price=ele.flight_fare
        ticket_price=int(base_price)*int(count)
        context={
            'count':count,
            'flight_class':flight_class,
            'flight':flight,
            'ticket_price':ticket_price
        }
        template=loader.get_template("result2.html")
        res=template.render(context,request)
        return HttpResponse(res)

def logout(request):
    del request.session['username'] #must destroy session keys
    template=loader.get_template("welcome.html")
    res=template.render()
    return HttpResponse(res)