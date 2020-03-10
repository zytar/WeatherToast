from collections import Counter
from win10toast import ToastNotifier
import requests
import json
import numpy as np
import urllib
from datetime import datetime, timedelta
from collections import defaultdict
#change lat and lon to your location and msl to your hight above sea level
def getWeather():
    url = 'https://api.met.no/weatherapi/locationforecast/1.9/.json'
    payload = {'lat': '50.378', 'lon': '9.329', 'msl': '1000'}
    r = requests.get(url, params=payload)
    ut = json.loads(r.content)
    return ut

def stringifyDateTime(date):
    strDate = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return strDate

def getDateInDays(days):
    date = datetime.now() + timedelta(days=days)
    return date

def getDateInDaysTimeStr(days):
    date = datetime.now() + timedelta(days=days)
    datestr = stringifyDateTime(date)
    return datestr

def dateify(date_string):
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")

def stringifyDate(date):
    strDate = date.strftime("%Y-%m-%d")
    return strDate


def getDateTemp(days):
    now = datetime.now()
    dateTo = getDateInDaysTimeStr(days)
    datetemp = defaultdict(list)
    ut = getWeather()
    times = ut['product']['time']
    for items in times:
        if items['to'] < dateTo:
            if 'temperature' in items['location']:
                datetemp[stringifyDate(dateify(items['to']))].append(float(items['location']['temperature']['value']))
    return(datetemp)

def Average(lst):
    return sum(lst) / len(lst)

def Notify(message):
    toaster = ToastNotifier()
    toaster.show_toast("Sjekk varmeldingen", message, duration=10, icon_path="snow.ico");

def NumberToDay(weekdaynumber):
    days = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    return (days[weekdaynumber])

def MakeMessage(temps):
    today = datetime.now()
    message = ""
    count = 0
    for temp in temps:
        time = today + timedelta(days=count)
        message = message + NumberToDay(time.weekday()) + ": " + str(round(temp,1)) + "     "
        if count % 2 == 1:
            message = message + "\n"
        count = count + 1
    return message

def MoreThanDays(days, forcastLength):
    datesAndTemps = getDateTemp(forcastLength)
    avgTemp = []
    count = 0

    for item in datesAndTemps:
        temps = datesAndTemps.get(item)
        avgTemp.append(Average(temps))

    for temp in avgTemp:
        if temp < 0:
            count = count+1
            break
        else:
            count = 0

    if count <= days:
        now = datetime.now()
        message = MakeMessage(avgTemp)
        Notify(message)



numberOfDays = 7
daysOfLowTempBeforeNotification = 3

MoreThanDays(daysOfLowTempBeforeNotification, numberOfDays)
