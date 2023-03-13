
from django.shortcuts import render, redirect
from .models import Input, Result, Intersection
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.

def uploadPage(request):
    d = timezone.now()
    if request.method == "GET":
        return render(request, "upload.html")
    if request.method == "POST" and (request.FILES.get('video') is not None ):
        ownerName = request.POST['ownerName']
        video = request.FILES['video']
        location = request.POST['location']
        intersection_name = request.POST['intersection_name'] if request.POST.get('intersection_name') is not None else ''
        time = request.POST.get('time') if request.POST.get('time') != "" else d.strftime("%H:%M:%S")
        date = request.POST.get('date') if request.POST.get('date') != "" else d.strftime("%Y-%m-%d")
        print(request.POST.get('traffic_status'))
        traffic_status = request.POST.get('traffic_status') if request.POST.get('traffic_status') is not None else 0
        note = request.POST['note'] if request.POST.get('note') is not None else ""
        weather = request.POST['weather'] if request.POST.get('weather') is not None else "Sunny"
        intersection = Intersection.objects.filter(name=intersection_name)
        if intersection:
            intersection = Intersection.objects.filter(name=intersection_name).get()    
        else:
            intersection = createIntersection(intersection_name)
    
        input = Input.objects.create(
            time_record=time, 
            date_record=date, 
            video=video,
            intersection = intersection, 
            location=location, 
            traffic_status=traffic_status, 
            note=note,
            weather=weather,  
            ownerName=ownerName
        )
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))

def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('home'))
            else:
                return uploadPage(request)
        else:
            return render(request, 'login.html', {
                'message': 'Invalid credentials.'
            }, status=400)

    return render(request, 'login.html')

def homeStatus(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginPage"))
    
def home(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        if searched:
            intersection_id = Intersection.objects.filter(name=searched).values_list('id', flat=True)
            task = Input.objects.filter(Q(intersection_id__in=intersection_id) | Q(location=searched)).all()
            return render(request, 'home.html', {'task': task,})
        else:
            task = Input.objects.all()
            return render(request, 'home.html', {'task': task,})
        
def delete(request, id):
    task = Input.objects.get(pk=id)
    task.delete()
    return HttpResponseRedirect(reverse('home'))

def edit(request, id):
    task = Input.objects.get(pk=id)
    d = timezone.now()
    if request.method=='POST' :
        task.ownerName = request.POST.get('ownerName')
        task.location = request.POST.get('location')
        # video = request.FILES.get('video') 
        # if video:
        #     task.video = video
        task.time_record = request.POST.get('time') if request.POST.get('time') != "" else d.strftime("%H:%M:%S")
        task.date_record = request.POST.get('date') if request.POST.get('date') != "" else d.strftime("%Y-%m-%d")
        intersection_name = request.POST['intersection'] if request.POST.get('intersection') is not None else ''
        intersection = Intersection.objects.filter(name=intersection_name)
        if intersection:
            intersection = Intersection.objects.filter(name=intersection_name).get()    
        else:
            intersection = createIntersection(intersection_name)
        task.intersection = intersection
        task.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'edit.html', {'edit': task, 'id':task.id})

def createIntersection(name):
    return Intersection.objects.create(name=name)

def generalInfo(request, id):
    result = Result.objects.filter(pk=id).get()
    input = Input.objects.filter(pk=result.input_video.pk).get()
    return render(request, 'generalInfo.html', {'result': result, 'input': input})

def edit_status(status, id):
    input = Input.objects.filter(pk=id).get()
    input.detect_status = status
    input.save()