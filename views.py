from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fb9f5aab7df9bb0f7aebffac65e9f55d"
    error_msg=""
    msg=''
    msg_class=''
    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            count=City.objects.filter(name=new_city).count()
            if count==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    error_msg="City Does not exist In this World!"
            else:
                error_msg="City alreday exists In  Your List"

        if error_msg:
            msg=error_msg
            msg_class='is-danger'
        else:
            msg="City Added Successfully In your List "
            msg_class='is-success'

    print(error_msg)
    form = CityForm()

    cities=City.objects.all()
    weather_data=[]

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather={
            'city':city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context={
            "weather_data":weather_data,
            'form':form,
            'msg': msg,
            'msg_class':msg_class,
        }
    return render(request, 'weather/weather.html',context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect("home")