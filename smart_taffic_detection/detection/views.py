
from django.shortcuts import render
from .models import Input, Result
from django.utils import timezone
# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def uploadPage(request):
    print(timezone.now().strftime('%H:%M:%S.%f')[:-3])
    if request.method == "GET":
        return render(request, "upload.html")
    if request.method == "POST" and (request.FILES.get('video') is not None ):
        video = request.FILES['video']
        location = request.POST['location']
        time = request.POST.get('time') if request.POST.get('time') is not None else timezone.now()
        date = request.POST.get('date') if request.POST.get('date') is not None else timezone.now()
        print(request.POST.get('traffic_status'))
        traffic_status = request.POST.get('traffic_status') if request.POST.get('traffic_status') is not None else 0
        note = request.POST['note'] if request.POST.get('note') is not None else ""
        weather = request.POST['weather'] if request.POST.get('weather') is not None else "Sunny"
        input = Input.objects.create(
            time_record=time, 
            date_record=date, 
            video=video, 
            location=location, 
            traffic_status=traffic_status, 
            note=note,
            weather=weather
        )
        return render(request, "upload.html", {'input': input})
    else:
        return render(request, "upload.html")
    

    