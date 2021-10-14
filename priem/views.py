from django.shortcuts import render
from priem.forms import RegisterForm
from priem.models import Register
from django.http import HttpResponse, HttpResponseNotFound
from priem.models import Stol
from priem.models import Holiday
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from priem.tables import PersonTable
from priem.forms import MyDateWidgetForm
from datetime import time
import requests
from django.db.models import Count
# Create your views here.

#https://www.youtube.com/watch?v=6vVnP02bkQc


def index(request):
    if request.method == "POST":
        reg = Register()
        # условие для предотвращения записи на один и тот же день, время и стол

        reg.fio = request.POST.get("fio")
        fio = request.POST.get("fio")

        reg.subject = request.POST.get("subject")
        subject = request.POST.get("subject")

        date = request.POST.get("r_date")

        d = datetime.strptime(date, '%d/%m/%Y')
        date1 = d.strftime('%Y-%m-%d')
        reg.r_date = date1
        reg.time = request.POST.get("time")
        time = request.POST.get("time")
        reg.stol = request.POST.get("stol")
        stol = request.POST.get("stol")
        check_day0 = check_work_day(date1)
        check_day=check_day0[0]
        check_day2 = check_day0[1]
        print("Проверки на рабочесть",check_day,'следующий',check_day2)
        holidays=check_employee_holydays(date1,stol)
        if Register.objects.filter(r_date=date1, time=time, stol=stol).count() == 0 \
                and check_day == 0 and check_day2 == 0 and holidays == 0:
            mes = HttpResponse("<h2>{0}, <p> Вы записаны в 32 кабинет на {1}<p>"
                               "Время {2} <p>"
                               "стол № {3}<p>"
                               "Причина обращения: {4}</h2>".format(fio,
                                                                    date, time, stol, subject))


            reg.save()
        elif Register.objects.filter(r_date=date1, time=time, stol=stol).count() == 0 \
                and check_day == 0 and check_day2 == 1 and holidays == 0:
            if time=='17:00':
                mes = HttpResponse("<h2>Записи на это время нет, предпраздничный день</h2>")
            elif time=='17:20':
                mes = HttpResponse("<h2>Записи на это время нет, предпраздничный день</h2>")
            elif time=='17:40':
                mes = HttpResponse("<h2>Записи на это время нет, предпраздничный день</h2>")
            else:
                mes = HttpResponse("<h2>{0}, <p> Вы записаны в 32 кабинет на {1}<p>"
                                   "Время {2} <p>"
                                   "стол № {3}<p>"
                                   "Причина обращения: {4}</h2>".format(fio,
                                                                        date, time, stol, subject))
                reg.save()

        elif holidays == 1:
            mes = HttpResponse("<h2>Записи нет, специалист в отпуске</h2>")

        else:
            if check_day == 1:
                mes = HttpResponse("<h2>Записи нет, это выходной</h2>")
            else:

                mes = HttpResponse("<h2>На это время уже есть запись</h2>")

        return mes
    else:
        user_form = RegisterForm()
        shot_date=search_free_date(request)
        #print('Ближайшая дата записи на прием: ',shot_date)
        return render(request, 'start.html', {'my_form': user_form,'s_date':shot_date})

def rec1(request):
    rd=datetime.today().strftime('%Y-%m-%d')
    people = Register.objects.filter(stol=1, r_date__gte=rd).order_by("r_date", "stol", "time")

    return render(request, 'rec1.html', {"people": people})


def rec2(request):
    rd = datetime.today().strftime('%Y-%m-%d')
    people = Register.objects.filter(stol=2, r_date__gte=rd).order_by("r_date", "stol", "time")

    return render(request, 'rec2.html', {"people": people})


def rec3(request):
    rd = datetime.today().strftime('%Y-%m-%d')
    people = Register.objects.filter(stol=3, r_date__gte=rd).order_by("r_date", "stol", "time")

    return render(request, 'rec3.html', {"people": people})


def rec4(request):
    rd = datetime.today().strftime('%Y-%m-%d')
    people = Register.objects.filter(stol=4, r_date__gte=rd).order_by("r_date", "stol", "time")

    return render(request, 'rec4.html', {"people": people})


def check_work_day(ddd):
    ddd2=datetime.strptime(ddd, '%Y-%m-%d')+timedelta(days=1)
    ddd3=datetime.strftime(ddd2, '%Y-%m-%d')
    #print(ddd3)
    stroka: object = ddd.split('-')
    URL = "https://isdayoff.ru/api/getdata"
    PARAMS = {'year': stroka[0], 'month': stroka[1], 'day': stroka[2]}
    r = requests.get(url=URL, params=PARAMS)
    # extracting data in json format
    data = r.json()
    stroka: object = ddd3.split('-')
    URL = "https://isdayoff.ru/api/getdata"
    PARAMS = {'year': stroka[0], 'month': stroka[1], 'day': stroka[2]}
    r = requests.get(url=URL, params=PARAMS)
    # extracting data in json format
    data2 = r.json()

    return data,data2

def date_from_ajax (request):
    if request.method == "POST" and request.is_ajax():
        date = request.POST.get("date_from_ajax")
        d = datetime.strptime(date, '%d/%m/%Y')
        date1 = d.strftime('%Y-%m-%d')
        reception_set = Register.objects.filter(r_date=date1)

        time_list=[]
        for reception in reception_set:
            time_list.append([reception.time,reception.stol])
        return JsonResponse({'time_list':time_list})


def delete(request, id):
    try:
        people = Register.objects.get(id=id)
        people.delete()

        return HttpResponseRedirect("/record.html")
    except Register.DoesNotExist:
        return HttpResponseNotFound("<h2>Запись не найдена</h2>")

def people(request):
    #people = PersonTable()
    rd = datetime.today().strftime('%Y-%m-%d')
    people = PersonTable(Register.objects.filter(r_date__gte=rd).order_by("r_date", "stol", "time"))
    return render(request, "record.html", {'people': people})

def check_employee_holydays(day,stol):
    rez = Holiday.objects.filter(stol=stol, date1__lte=day , date2__gte=day).count()
    #print(rez)
    if rez > 0:
        a = 1
        #print("holiday")
    else:
        #print("Work")
        a = 0
    return a


def stol(request):
    stol=Stol.objects.all()
    return render(request, "stol.html",{"stol": stol})

def stol_create(request):
    if request.method == "POST":
        stol = Stol()
        stol.fio = request.POST.get("fio")
        stol.stol = request.POST.get("stol")
        stol.save()

    return HttpResponseRedirect('/stol.html')

def stol_delete(request, id):
    try:
        stol = Stol.objects.get(id=id)
        stol.delete()

        return HttpResponseRedirect("/stol.html")
    except Register.DoesNotExist:
        return HttpResponseNotFound("<h2>Запись не найдена</h2>")


def holiday(request):
    date_form = MyDateWidgetForm()
    holidays = Holiday.objects.all()
    return render(request, "holiday.html", {'hol_form': date_form, 'holidays': holidays})

def holiday_create(request):
    if request.method == "POST":
        holiday = Holiday()
        holiday.stol = request.POST.get("stol")
        holiday.fio =Stol.objects.get(stol=holiday.stol)
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        d1 = datetime.strptime(date1, '%d/%m/%Y')
        d2 = datetime.strptime(date2, '%d/%m/%Y')
        date1 = d1.strftime('%Y-%m-%d')
        date2 = d2.strftime('%Y-%m-%d')
        holiday.date1 = date1
        holiday.date2 = date2

        holiday.save()
    return HttpResponseRedirect('/holiday.html')

def holiday_delete(request, id):
    try:
        holiday = Holiday.objects.get(id=id)
        holiday.delete()

        return HttpResponseRedirect("/holiday.html")
    except Register.DoesNotExist:
        return HttpResponseNotFound("<h2>Запись не найдена</h2>")


def search_free_date(request):
    rd = datetime.today().strftime('%Y-%m-%d')
    q1 = Register.objects.filter(r_date__gte=rd).order_by("r_date")
    q2 = q1.values('r_date','stol').annotate(nstol=Count('stol'))

    #answers_list = list(q2.values('r_date','stol','nstol'))
    result1 = q2.values('r_date')
    result2 = q2.values('stol')
    result3 = q2.values('nstol')

    list_result1 = [entry for entry in result1]
    list_result2 = [entry for entry in result2]
    list_result3 = [entry for entry in result3]

    for i in range(len(list_result3)):
        str = list_result3[i]
        m = str['nstol']
        if m < 24:
            #print(m)
            stol=list_result2[i]['stol']
            #print(stol)
            data=list_result1[i]['r_date']
            #print(data)
            h = check_employee_holydays(data, stol)
            if h == 0:
                #print('Ближайший день:', data)

                return data


