from .models import Input, Result, Intersection, CreateLoop

def edit_status(status, id):
    input = Input.objects.filter(pk=id).get()
    input.detect_status = status
    input.save()

import matplotlib.patches as patches
from PIL import Image
from .task import call_detect
from django.shortcuts import render, redirect
from django.conf import settings
import cv2
import numpy as np
import uuid
import io
import shutil
import os
import json
import math
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# from celery.result import AsyncResult
# from django.http import JsonResponse
# Create your views here.

def createLoop(request, id):
    plt.clf()
    if request.method == 'POST':
        fileName = request.POST['fileName']

        loopName1 = request.POST['loopName1']
        x1 = request.POST['x1']
        y1 = request.POST['y1']
        width1 = request.POST['width1']
        height1 = request.POST['height1']
        angle1 = request.POST['angle1']

        loopName2 = request.POST['loopName2']
        x2 = request.POST['x2']
        y2 = request.POST['y2']
        width2 = request.POST['width2']
        height2 = request.POST['height2']
        angle2 = request.POST['angle2']

        loopName3 = request.POST['loopName3']
        x3 = request.POST['x3']
        y3 = request.POST['y3']
        width3 = request.POST['width3']
        height3 = request.POST['height3']
        angle3 = request.POST['angle3']

        loopName4 = request.POST['loopName4']
        x4 = request.POST['x4']
        y4 = request.POST['y4']
        width4 = request.POST['width4']
        height4 = request.POST['height4']
        angle4 = request.POST['angle4']

        # Create the directory if it does not exst
        directory = 'exports'
        if not os.path.exists(directory):
            os.makedirs(directory)
        x1=int(x1)
        y1=int(y1)
        x2=int(x2)
        y2=int(y2)
        x3=int(x3)
        y3=int(y3)
        x4=int(x4)
        y4=int(y4)
        width1 = int(width1)
        width2 = int(width2)
        width3 = int(width3)
        width4 = int(width4)
        height1 = int(height1)
        height2 = int(height2)
        height3 = int(height3)
        height4 = int(height4)
        angle1 = int(angle1)
        angle2 = int(angle2)
        angle3 = int(angle3)
        angle4 = int(angle4)

        xtl1, ytl1 = x1, y1
        xtr1, ytr1 = x1 + width1 * np.cos(angle1), y1 + width1 * np.sin(angle1)
        xbr1, ybr1 = x1 - height1 * np.sin(angle1), y1 + height1 * np.cos(angle1)
        xbl1 , ybl1 = x1 + width1 * np.cos(angle1) - height1 * np.sin(angle1), y1 + width1 * np.sin(angle1) + height1 * np.cos(angle1)
        
        xtl2, ytl2 = x2, y2
        xtr2, ytr2 = x2 + width2 * np.cos(angle2), y2 + width2 * np.sin(angle2)
        xbr2, ybr2 = x2 - height2 * np.sin(angle2), y2 + height2 * np.cos(angle2)
        xbl2 , ybl2 = x2 + width2 * np.cos(angle2) - height2 * np.sin(angle2), y2 + width2 * np.sin(angle2) + height2 * np.cos(angle2)
        
        xtl3, ytl3 = x3, y3
        xtr3, ytr3 = x3 + width3 * np.cos(angle3), y3 + width3 * np.sin(angle3)
        xbr3, ybr3 = x3 - height3 * np.sin(angle3), y3 + height3 * np.cos(angle3)
        xbl3 , ybl3 = x3 + width3 * np.cos(angle3) - height3 * np.sin(angle3), y3 + width3 * np.sin(angle3) + height3 * np.cos(angle3)
        
        xtl4, ytl4 = x4, y4
        xtr4, ytr4 = x4 + width4 * np.cos(angle4), y4 + width4 * np.sin(angle4)
        xbr4, ybr4 = x4 - height4 * np.sin(angle4), y4 + height4 * np.cos(angle4)
        xbl4 , ybl4 = x4 + width4 * np.cos(angle4) - height4 * np.sin(angle4), y4 + width4 * np.sin(angle4) + height4 * np.cos(angle4)

        # Write the data to a JSON file
        json_data = {
            'loops': [
                {
                    'name': loopName1,
                    'id':"0",
                    'points':[
                        {"x": int(xtl1), "y": int(ytl1)},
                        {"x": int(xtr1), "y": int(ytr1)},
                        {"x": int(xbl1), "y": int(ybl1)},
                        {"x": int(xbr1), "y": int(ybr1)},
                    ],
                    'orientation':"counterclockwise",
                    "summary_location":{"x":0,"y":"30"},
                },
                {
                    'name': loopName2,
                    'id':"1",
                    'points':[
                        {"x": int(xbl2), "y": int(ybl2)},
                        {"x": int(xtr2), "y": int(ytr2)},
                        {"x": int(xtl2), "y": int(ytl2)},
                        {"x": int(xbr2), "y": int(ybr2)}
                    ],
                    'orientation':"clockwise",
                    "summary_location":{"x":950,"y":"30"},
                },
                {
                    'name': loopName3,
                    'id':"2",
                    'points':[
                        {"x": int(xbl3), "y": int(ybl3)},
                        {"x": int(xbr3), "y": int(ybr3)},
                        {"x": int(xtl3), "y": int(ytl3)},
                        {"x": int(xtr3), "y": int(ytr3)}
                    ],
            
                    'orientation':"counterclockwise",
                    "summary_location":{"x":950,"y":"370"},
                },
                {
                    'name': loopName4,
                    'id':"3",
                    'points':[
                        {"x": int(xtl4), "y": int(ytl4)},
                        {"x": int(xbr4), "y": int(ybr4)},
                        {"x": int(xbl4), "y": int(ybl4)},
                        {"x": int(xtr4), "y": int(ytr4)}
                    ],
                    'orientation':"counterclockwise",
                    "summary_location":{"x":0,"y":"370"},
                },
            ]
        }

        # Write the JSON data to a file
        json_file_path = os.path.join(directory, f'{fileName}.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)
        
        # Create a copy of the JSON file in the "arial-car-track" folder
        json_copy_path = os.path.join('arial-car-track', 'loop.json')
        shutil.copyfile(json_file_path, json_copy_path)

        # Write the formatted data to a text file
        text_file_path = os.path.join(directory, f'{fileName}.txt')
        with open(text_file_path, 'w') as f:
            f.write(f'{x1}, {y1}, {width1}, {height1}, {angle1}\n')
            f.write(f'{x2}, {y2}, {width2}, {height2}, {angle2}\n')
            f.write(f'{x3}, {y3}, {width3}, {height3}, {angle3}\n')
            f.write(f'{x4}, {y4}, {width4}, {height4}, {angle4}\n')

        loop = CreateLoop(
            fileName = fileName, loopName1=loopName1, x1=x1, y1=y1, width1=width1, height1=height1,angle1=angle1,
            loopName2=loopName2, x2=x2, y2=y2, width2=width2, height2=height2,angle2=angle2,
            loopName3=loopName3, x3=x3, y3=y3, width3=width3, height3=height3,angle3=angle3,
            loopName4=loopName4, x4=x4, y4=y4, width4=width4, height4=height4,angle4=angle4,
            )
        loop.save()
        input = Input.objects.get(id=id)
        input.loop = loop
        input.save()
        
        select_draw(f'{fileName}.txt' , id)
        return redirect('preview')
    
    return render(request, 'loop.html')

def edit_loop(request, id):
    input = Input.objects.get(id=id)
    loop = CreateLoop.objects.get(id=input.loop.pk)

    if request.method == 'POST':
        print("It post")
        
        loop.loopName1 = request.POST.get('loopName1')
        loop.x1 = request.POST.get('x1')
        loop.y1 = request.POST.get('y1')
        loop.width1 = request.POST.get('width1')
        loop.height1 = request.POST.get('height1')
        loop.angle1 = request.POST.get('angle1')

        loop.loopName2 = request.POST.get('loopName2')
        loop.x2 = request.POST.get('x2')
        loop.y2 = request.POST.get('y2')
        loop.width2 = request.POST.get('width2')
        loop.height2 = request.POST.get('height2')
        loop.angle2 = request.POST.get('angle2')

        loop.loopName3 = request.POST.get('loopName3')
        loop.x3 = request.POST.get('x3')
        loop.y3 = request.POST.get('y3')
        loop.width3 = request.POST.get('width3')
        loop.height3 = request.POST.get('height3')
        loop.angle3 = request.POST.get('angle3')

        loop.loopName4 = request.POST.get('loopName4')
        loop.x4 = request.POST.get('x4')
        loop.y4 = request.POST.get('y4')
        loop.width4 = request.POST.get('width4')
        loop.height4 = request.POST.get('height4')
        loop.angle4 = request.POST.get('angle4')
        loop.save()

        x1=int(loop.x1)
        y1=int(loop.y1)
        x2=int(loop.x2)
        y2=int(loop.y2)
        x3=int(loop.x3)
        y3=int(loop.y3)
        x4=int(loop.x4)
        y4=int(loop.y4)
        width1 = int(loop.width1)
        width2 = int(loop.width2)
        width3 = int(loop.width3)
        width4 = int(loop.width4)
        height1 = int(loop.height1)
        height2 = int(loop.height2)
        height3 = int(loop.height3)
        height4 = int(loop.height4)
        angle1 = int(loop.angle1)
        angle2 = int(loop.angle2)
        angle3 = int(loop.angle3)
        angle4 = int(loop.angle4)

        
        xtl1, ytl1 = x1, y1
        xtr1, ytr1 = x1 + width1 * np.cos(angle1), y1 + width1 * np.sin(angle1)
        xbr1, ybr1 = x1 - height1 * np.sin(angle1), y1 + height1 * np.cos(angle1)
        xbl1 , ybl1 = x1 + width1 * np.cos(angle1) - height1 * np.sin(angle1), y1 + width1 * np.sin(angle1) + height1 * np.cos(angle1)
        
        xtl2, ytl2 = x2, y2
        xtr2, ytr2 = x2 + width2 * np.cos(angle2), y2 + width2 * np.sin(angle2)
        xbr2, ybr2 = x2 - height2 * np.sin(angle2), y2 + height2 * np.cos(angle2)
        xbl2 , ybl2 = x2 + width2 * np.cos(angle2) - height2 * np.sin(angle2), y2 + width2 * np.sin(angle2) + height2 * np.cos(angle2)
        
        xtl3, ytl3 = x3, y3
        xtr3, ytr3 = x3 + width3 * np.cos(angle3), y3 + width3 * np.sin(angle3)
        xbr3, ybr3 = x3 - height3 * np.sin(angle3), y3 + height3 * np.cos(angle3)
        xbl3 , ybl3 = x3 + width3 * np.cos(angle3) - height3 * np.sin(angle3), y3 + width3 * np.sin(angle3) + height3 * np.cos(angle3)
        
        xtl4, ytl4 = x4, y4
        xtr4, ytr4 = x4 + width4 * np.cos(angle4), y4 + width4 * np.sin(angle4)
        xbr4, ybr4 = x4 - height4 * np.sin(angle4), y4 + height4 * np.cos(angle4)
        xbl4 , ybl4 = x4 + width4 * np.cos(angle4) - height4 * np.sin(angle4), y4 + width4 * np.sin(angle4) + height4 * np.cos(angle4)

        data = {
            'loops': [
                {
                    'name': loop.loopName1,
                    'id':"0",
                    'points':[
                        {"x": int(xtl1), "y": int(ytl1)},
                        {"x": int(xtr1), "y": int(ytr1)},
                        {"x": int(xbl1), "y": int(ybl1)},
                        {"x": int(xbr1), "y": int(ybr1)},
                    ],
                    'orientation':"counterclockwise",
                    "summary_location":{"x":0,"y":"30"},
                },
                {
                    'name': loop.loopName2,
                    'id':"1",
                    'points':[
                        {"x": int(xbl2), "y": int(ybl2)},
                        {"x": int(xtr2), "y": int(ytr2)},
                        {"x": int(xtl2), "y": int(ytl2)},
                        {"x": int(xbr2), "y": int(ybr2)}
                    ],
                    'orientation':"clockwise",
                    "summary_location":{"x":950,"y":"30"},
                },
                {
                    'name': loop.loopName3,
                    'id':"2",
                    'points':[
                        {"x": int(xbl3), "y": int(ybl3)},
                        {"x": int(xbr3), "y": int(ybr3)},
                        {"x": int(xtl3), "y": int(ytl3)},
                        {"x": int(xtr3), "y": int(ytr3)}
                    ],
            
                    'orientation':"counterclockwise",
                    "summary_location":{"x":950,"y":"370"},
                },
                {
                    'name': loop.loopName4,
                    'id':"3",
                    'points':[
                        {"x": int(xtl4), "y": int(ytl4)},
                        {"x": int(xbr4), "y": int(ybr4)},
                        {"x": int(xbl4), "y": int(ybl4)},
                        {"x": int(xtr4), "y": int(ytr4)}
                    ],
                    'orientation':"counterclockwise",
                    "summary_location":{"x":0,"y":"370"},
                },
            ]
        }
        
        file_path = os.path.join('exports', f'{loop.fileName}.json')
        with open(file_path, 'w') as f:
            json.dump(data, f)
            
        text_file_path = os.path.join('exports', f'{loop.fileName}.txt')
        with open(text_file_path, 'w') as f:
            f.write(f'{loop.x1}, {loop.y1}, {loop.width1}, {loop.height1}, {loop.angle1}\n')
            f.write(f'{loop.x2}, {loop.y2}, {loop.width2}, {loop.height2}, {loop.angle2}\n')
            f.write(f'{loop.x3}, {loop.y3}, {loop.width3}, {loop.height3}, {loop.angle3}\n')
            f.write(f'{loop.x4}, {loop.y4}, {loop.width4}, {loop.height4}, {loop.angle4}\n')
        plt.clf()
        select_draw(f'{loop.fileName}.txt' , id)

    context = {
        'loop': loop,
        'id': loop.id,
        'input': input, 
    }
    return render(request, 'editLoop.html', context)

def preview(request):
    loop = CreateLoop.objects.all()
    task = Input.objects.all()
    return render(request, 'preview.html', {'loop': loop, 'task': task})

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
            image_rescaled = cv2.resize(image, (0, 0), fx=1.0, fy=1.0)
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
def detect(request, id):
    input = Input.objects.get(id=id)
    print(input.video.url)
    h,media, url = input.video.url.split('/')
    result = call_detect.delay('./media/uploads/video/' + url, input.pk)
    return HttpResponseRedirect(reverse('home'))

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


def drawFourLoop(loop1,loop2,loop3,loop4,id):
        plt.clf()
        input = Input.objects.get(id=id)
        print(f'{input.image_scale}')
        image_path = os.path.join(settings.MEDIA_ROOT,  str(input.image))
        filename, ext = os.path.splitext(input.image.name)
        image_path2 = os.path.join(settings.MEDIA_ROOT, f'{filename}_draw.jpg' )
        drawing_image = np.array(Image.open(image_path))
        plt.imshow(drawing_image)
        plt.gca().add_patch(
                plt.Rectangle([loop1[0],loop1[1]],
                            loop1[2],loop1[3],
                            fill=False,
                            color='blue',
                            angle = loop1[4],
                            alpha=1)
                )
        plt.gca().add_patch(
                plt.Rectangle([loop2[0],loop2[1]],
                            loop2[2],loop2[3],
                            fill=False,
                            color='green',
                            angle = loop2[4],
                            alpha=1)
                )
        plt.gca().add_patch(
                plt.Rectangle([loop3[0],loop3[1]],
                            loop3[2],loop3[3],
                            fill=False,
                            color='red',
                            angle = loop3[4],
                            alpha=1)
                )
        plt.gca().add_patch(
                plt.Rectangle([loop4[0],loop4[1]],
                            loop4[2],loop4[3],
                            fill=False,
                            color='yellow',
                            angle = loop4[4],
                            alpha=1)
                )
        plt.savefig(image_path2)
        input.image_draw = f'{filename}_draw.jpg'
        input.save()
        return print("drawFourLoop Finish")

def select_draw(name ,id):

    text_file_path = os.path.join('exports' , name)     
    with open(text_file_path, 'r') as f:
        line_count = len(f.readlines())
        f.close()
    with open(text_file_path, 'r') as f:
        if line_count == 4:
            lines = f.readlines()
            data_first_line = lines[0].strip().split(',')  # แยกค่าข้อมูลในบรรทัดเป็น list สตริง
            data_float1 = [float(d) for d in data_first_line]  # แปลงค่าใน list เป็นตัวเลข float
            data_float1 = data_float1[:-1] + [-data_float1[-1]]
            data_second_line = lines[1].strip().split(',')  
            data_float2 = [float(d) for d in data_second_line] 
            data_third_line = lines[2].strip().split(',')  
            data_float3 = [float(d) for d in data_third_line]
            data_float3 = data_float3[:-1] + [-data_float3[-1]]
            data_fourth_line = lines[3].strip().split(',')  
            data_float4 = [float(d) for d in data_fourth_line]  
            loop1 , loop2 , loop3 , loop4 = data_float1 ,data_float2 ,data_float3 ,data_float4
            drawFourLoop(loop1,loop2,loop3,loop4,id)
    f.close()


