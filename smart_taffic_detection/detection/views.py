
from django.shortcuts import render
from .models import Input, Result

# Create your views here.

def uploadPage(request):
    if request.method == "GET":
        return render(request, "upload.html")
    if request.method == "POST" and (request.FILES.get('video') is not None ):
        print(request.FILES)
        video = request.FILES['video']
        print(video)
        location = request.POST['location']
        input = Input.objects.create(video=video, location=location)
        return render(request, "upload.html")
    else:
        return render(request, "upload.html")


    