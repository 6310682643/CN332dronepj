from django.shortcuts import render
from django.urls import reverse
from .models import Video
from .form import Video_form
from django.shortcuts import HttpResponse, HttpResponseRedirect


# Create your views here.
def homepage(request):
    return render(request, "detect/homepage.html")

def uploaddata(request):
    all_video = Video.objects.all()
    if request.method == "POST":
        form = Video_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse("homepage"))
    else:
        form = Video_form()
    return render(request, "detect/upload.html", {"form":form,"all": all_video})

def clip_detect(request):
    video = Video.objects.all()
    return render(request, "detect/general_info.html", {"video": video})

