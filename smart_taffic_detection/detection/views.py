from .task import call_detect
from django.shortcuts import render, redirect
from .models import Input, Result
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
# from celery.result import AsyncResult
# from django.http import JsonResponse
# Create your views here.


def uploadPage(request):
    print(timezone.now().strftime('%H:%M:%S.%f')[:-3])
    d = timezone.now()
    if request.method == "GET":
        return render(request, "upload.html")
    if request.method == "POST" and (request.FILES.get('video') is not None):
        ownerName = request.POST['ownerName']
        video = request.FILES['video']
        location = request.POST['location']
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
        
        input = Input.objects.create(
            time_record=time,
            date_record=date,
            video=video,
            location=location,
            traffic_status=traffic_status,
            note=note,
            weather=weather,
            ownerName=ownerName
        )

        result = call_detect.delay('./' + input.video.url)

        return HttpResponseRedirect(reverse('home'))
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


def homeStatus(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginPage"))


def home(request):
    task = Input.objects.all()
#   template = loader.get_template('home.html')
    return render(request, 'home.html', {'task': task, })


def delete(request, id):
    task = Input.objects.get(pk=id)
    task.delete()
    return redirect('home')


# def searchBar(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("login"))
#     user_id = request.user.id

#     if request.method == "GET":
#         searched = request.GET.get('searched')
#         if searched:
#             blogs = Blog.objects.filter(title__contains=searched)
#             return render(request, 'users/searchfor.html', {'blogs': blogs})
#         else:
#             print("No information to show")
#             return render(request, 'users/searchfor.html', {'wallet':wallet})
