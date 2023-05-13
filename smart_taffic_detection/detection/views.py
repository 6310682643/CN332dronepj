from .models import Input, Result, Intersection

def edit_status(status, id):
    input = Input.objects.filter(pk=id).get()
    input.detect_status = status
    input.save()

from .task import call_detect
from django.shortcuts import render, redirect
from django.conf import settings
import cv2
import numpy as np
import uuid
import io
import os
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

import matplotlib.pyplot as plt
# from celery.result import AsyncResult
# from django.http import JsonResponse
# Create your views here.



def createLoop(request, id):
    task = Input.objects.get(pk=id)
    if request.method == "POST":
        loopName = request.POST['loopName']
        x = request.POST['x']
        y = request.POST['y']
        return render(request, "loop.html", {'loop': task, 'id': task.id})
    if request.method == "GET":
        return render(request, "loop.html", {'loop': task, 'id': task.id})

def uploadPage(request):
    print(timezone.now().strftime('%H:%M:%S.%f')[:-3])
    d = timezone.now()
    if request.method == "GET":
        return render(request, "upload.html", {'choice': Input.choices})
    if request.method == "POST" and (request.FILES.get('video') is not None):
        ownerName = request.POST['ownerName']
        video = request.FILES.get('video')
        location = request.POST['location']
        intersection_name = request.POST['intersection_name'] if request.POST.get(
            'intersection_name') is not None else ''
        time = request.POST.get('time') if request.POST.get(
            'time') != "" else d.strftime("%H:%M:%S")
        date = request.POST.get('date') if request.POST.get(
            'date') != "" else d.strftime("%Y-%m-%d")
        print(request.POST.get('traffic_status'))
        traffic_status = request.POST.get('traffic_status') if request.POST.get(
            'traffic_status') is not None else 0
        note = request.POST['note'] if request.POST.get(
            'note') is not None else ""
        weather = request.POST['weather'] if request.POST.get(
            'weather') is not None else "Sunny"
        intersection = Intersection.objects.filter(name=intersection_name)
        if intersection:
            intersection = Intersection.objects.filter(
                name=intersection_name).get()
        else:
            intersection = createIntersection(intersection_name)

        # Generate a unique identifier using the uuid module
        unique_id = str(uuid.uuid4())[:8]
    
        # Append the unique identifier to the video name
        video_name = f"{video.name.split('.')[0]}_{unique_id}.mp4"


        # new code open cv
        video_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'video', video_name)
        
        with open(video_path, 'wb') as f:
            for chunk in video.chunks():
                f.write(chunk)


        cap = cv2.VideoCapture(video_path)
        success, image = cap.read()
        
        if success:
            image_name = f"{video_name}.png"
            image_path = os.path.join(settings.MEDIA_ROOT, 'uploads/images', image_name)
            
            cv2.imwrite(image_path, image) # Save default image
            
            # Rescale the image and save it with a different name
            image_rescaled = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            image_name_scale = f"{video_name}_scale.png"
            image_path_scale = os.path.join(settings.MEDIA_ROOT, 'uploads/images', image_name_scale)
            
            plt.imshow(image_rescaled)
            plt.savefig(image_path_scale) # Save rescaled image using matplotlib
            
        else:
            print("fail to upload")
            

        input = Input.objects.create(
            time_record=time,
            date_record=date,
            video=video_name,
            image=f'uploads/images/{image_name}',
            image_scale=f'uploads/images/{image_name_scale}',
            intersection=intersection,
            location=location,
            traffic_status=traffic_status,
            note=note,
            weather=weather,
            ownerName=ownerName,
        
        )
     
                     
        

        # result = call_detect.delay('./' + input.video.url, input.pk)

        # return HttpResponseRedirect(reverse('createLoop'))
        return render(request, "loop.html", {'id': input.pk, 'input': input})
    else:
        return render(request, "upload.html")

# def celery_status(request, task_id):
#     result = AsyncResult(task_id)
#     response = {'status': result.status}
#     return JsonResponse(response)

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

def home(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        if searched:
            intersection_id = Intersection.objects.filter(
                name=searched).values_list('id', flat=True)
            task = Input.objects.filter(
                Q(intersection_id__in=intersection_id) | Q(location=searched)).all()
            return render(request, 'home.html', {'task': task, })
        else:
            task = Input.objects.all()
            return render(request, 'home.html', {'task': task, })


def delete(request, id):
    task = Input.objects.get(pk=id)
    task.delete()
    return HttpResponseRedirect(reverse('home'))


def edit(request, id):
    task = Input.objects.get(pk=id)
    d = timezone.now()
    if request.method == 'POST':
        task.ownerName = request.POST.get('ownerName')
        task.location = request.POST.get('location')
        # video = request.FILES.get('video')
        # if video:
        #     task.video = video
        task.time_record = request.POST.get('time') if request.POST.get(
            'time') != "" else d.strftime("%H:%M:%S")
        task.date_record = request.POST.get('date') if request.POST.get(
            'date') != "" else d.strftime("%Y-%m-%d")
        intersection_name = request.POST['intersection'] if request.POST.get(
            'intersection') is not None else ''
        intersection = Intersection.objects.filter(name=intersection_name)
        if intersection:
            intersection = Intersection.objects.filter(
                name=intersection_name).get()
        else:
            intersection = createIntersection(intersection_name)
        task.intersection = intersection
        task.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'edit.html', {'edit': task, 'id': task.id})


def createIntersection(name):
    return Intersection.objects.create(name=name)


def generalInfo(request, id):
    input = Input.objects.filter(pk=id).get()
    result = Result.objects.filter(input_video_id=input.pk).first()
    return render(request, 'generalInfo.html', {'result': result, 'input': input})


