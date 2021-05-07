from django.shortcuts import render, redirect, get_object_or_404
from LOGIN.models import Person, Feed, Booking, Workshop, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import CreateInDiscussion, PersonForm, UserUpdateForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver


def Indexpage(request):
    return render(request,'index.html')

def homepage(request):
    person = Person.objects.filter(Email=request.session['Email'])
    return render(request, 'homepage.html',{'person': person })




#user registration
def UserReg(request):
    if request.method=='POST':
        Email=request.POST['Email']
        Pwd=request.POST['Pwd']
        Username=request.POST.get('Username')
        Name=request.POST.get('Name')
        DateOfBirth=request.POST.get('DateOfBirth')
        Age=request.POST['Age']
        District=request.POST['District']
        State=request.POST['State']
        Occupation=request.POST['Occupation']
        About=request.POST['About']
        Gen=request.POST.get('Gender')
        MaritalStatus=request.POST.get('MaritalStatus')
        Person(Email=Email,Password=Pwd,Username=Username,Name=Name,DateOfBirth=DateOfBirth,Age=Age,District=District,State=State,
            Occupation=Occupation,About=About,Gender=Gen,MaritalStatus=MaritalStatus).save(),
        messages.success(request,'The new user ' + request.POST['Username'] + " is save succesfully..!")
        return render(request,'registration.html')
    else :
        return render(request,'registration.html')

def loginpage(request):
    if request.method=="POST":
        try:
            Userdetails=Person.objects.get(Email=request.POST['Email'],Password=request.POST['Pwd'])
            print("Username",Userdetails)
            request.session['Email']=Userdetails.Email
            person = Person.objects.filter(Email=request.POST['Email'])
            return render(request,'homepage.html',{'person': person})
        except Person.DoesNotExist as e:
            messages.success(request,'Username/Password Invalid..!')
    return render(request,'login.html')

def logout(request):
    try:
        del request.session['Email']
    except:
        return render(request,'index.html')
    return render(request,'index.html')



#profile
def view(request):
    person = Person.objects.filter(Email=request.session['Email'])
    if request.method=='POST':
       t = Person.objects.get(Email=request.session['Email'])
       t.Password=request.POST['Password']
       t.Username=request.POST.get('Username')
       t.Name=request.POST.get('Name')
       t.DateOfBirth=request.POST.get('DateOfBirth')
       t.Age=request.POST['Age']
       t.District=request.POST['District']
       t.State=request.POST['State']
       t.Occupation=request.POST['Occupation']
       t.About=request.POST['About']
       t.Gen=request.POST.get('Gender')
       t.MaritalStatus=request.POST.get('MaritalStatus')
       t.save()
       return render(request,'homepage.html')
    else:
        return render(request, 'profile.html',{'person': person})  





#sharing
def mainSharing(request):
    try:
        feed=Feed.objects.all()
        return render(request,'MainSharing.html',{'feed':feed})
    except Feed.DoesNotExist:
        raise Http404('Data does not exist')

def sharing(request):
    if request.method=='POST':
        Title=request.POST.get('Title')
        Message=request.POST.get('Message')
        Photo=request.POST.get('Photo')
        Video=request.POST.get('Video')
        Graph=request.POST.get('Graph')
        Feed(Title=Title,Message=Message,Photo=Photo,Video=Video,Graph=Graph).save(),
        messages.success(request,'The new feed is save succesfully..!')
        return render(request,'sharing.html')
    else :
        return render(request,'sharing.html')

#def viewSharing(request):
    #eed = Feed.objects.all()
    #return render(request,'ViewSharing.html',{'feed':feed})  

def updateSharing(request):
    #feed = Feed.objects.filter(Title=request.session['Title'])
    if request.method=='POST':
       f = Feed.objects.get(Title=request.session['Title'])
       f.Title=request.POST['Title']
       f.Message=request.POST.get('Message')
       f.Photo=request.POST.get('Photo')
       f.Video=request.POST.get('Video')
       f.Graph=request.POST['Graph']
       f.save()
       return render(request,'ViewSharing.html')
    else:
        return render(request, 'homepage.html',{'feed': feed})  

def deleteSharing(request,id):
    sharing = get_object_or_404(sharing, id=id)
    if request.method=='POST':
        sharing.delete()
        return redirect('homepage.html')
    context = {
        "object" : sharing
    }
    return render(request, 'deleteSharing.html', {'object':sharing})

    #feed_id = int(feed_id)
    #try:
    #    feed_sel = Feed.objects.get(id = feed_id)
    #except Feed.DoesNotExist:
    #    return redirect('index')
    #feed_sel.delete()
    #return redirect('index')





#group
def mainGroup(request):
    try:
        group=Group.objects.all()
        return render(request,'MainGroup.html',{'group':group})
    except Group.DoesNotExist:
        raise Http404('Data does not exist')

def group(request):
    if request.method=='POST':
        Name=request.POST.get('Name')
        About=request.POST.get('About')
        Media=request.POST.get('Media')
        Group(Name=Name,About=About,Media=Media).save(),
        messages.success(request,'The new group ' + request.POST['Name'] + " is create succesfully..!")
        return render(request,'group.html')
    else :
        return render(request,'group.html')

def myGroup(request):
    #try:
    #    group=Group.objects.filter(Name=request.session['Name'])
        return render(request,'MyGroup.html')#{'group':group})
    #except Group.DoesNotExist:
     #   raise Http404('Data does not exist')




#discussion
def viewdiscussion(request):
    if request.method=='POST':
        About=request.POST.get('About')
        Discussion=request.POST.get('Discussion')
        Media=request.POST.get('Media')
        Name=request.POST.get('Name')
        Discussion(About=About,Discussion=Discussion,Name=Name).save(),
        return render(request,'/home.html')
    else :
        return render(request,'discussion.html')

def discussion(request):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        context ={'form':form}
    return render(request,'group.html')






#workshop
def workshop(request):
        try:
            data=Workshop.objects.all()
            return render(request,'workshop.html',{'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')
            
def createWorkshop(request):
    if request.method=='POST':
        ProgrammeName=request.POST.get('ProgrammeName')
        Description=request.POST.get('Description')
        Date=request.POST.get('Date')
        Session=request.POST.get('Session')
        Workshop(ProgrammeName=ProgrammeName,Description=Description,Date=Date,Session=Session).save(),
        messages.success(request,'The ' + request.POST['ProgrammeName'] + " is save succesfully..!")
        return render(request,'CreateWorkshop.html')
    else :
        return render(request,'CreateWorkshop.html')

def booking(request):
    #person = Person.objects.filter(Email=request.session['Email'])
    #return render(request, 'booking.html',{'person': person})

    try:
        data=Workshop.objects.all() #filter(ProgrammeName=request.session['ProgrammeName'])
        return render(request,'booking.html',{'data':data})
    except Workshop.DoesNotExist:
        raise Http404('Data does not exist')

    #if request.method=='POST':
    #    ProgrammeName=request.POST.get('ProgrammeName')
    #    Date=request.POST.get('Date')
     #   Session=request.POST.get('Session')
     #   Workshop(ProgrammeName=ProgrammeName,Date=Date,Session=Session).save(),
     #   messages.success(request,'The booking of ' + request.POST['ProgrammeName'] + " is save succesfully..!")
     #   return render(request,'booking.html')
    #else :
     #   return render(request,'booking.html')

    #data = Workshop.objects.all#filter(ProgrammeName=request.session['ProgrammeName'])
    #return render(request, 'booking.html',{'data': data})



















































