import time
from zoneinfo import ZoneInfo
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loaders import cached

from .models import *
from datetime import timedelta
import datetime
import json
from django.utils import timezone
import requests
from django.http import JsonResponse

train_timings_harborfront = []

def main(request, action=None):
    Coordinates = {}

    # bus stop amenity and train station have longitude, latitude
    # queries each type of amenity, adds it to the dictionary
    ATMsBuses = BusStopAmenity.objects.filter(Amenity="ATM")
    ATMsTrains = TrainStationAmenity.objects.filter(Amenity="ATM")
    ATMs = ATMsBuses.union(ATMsTrains)

    ConvenienceBuses = BusStopAmenity.objects.filter(Amenity="Convenience Store")
    ConvenienceTrains = TrainStationAmenity.objects.filter(Amenity="Convenience Store")
    Conveniences = ConvenienceTrains.union(ConvenienceBuses)

    WheelchairBuses = BusStopAmenity.objects.filter(Amenity="Wheelchair")
    WheelchairTrains = TrainStationAmenity.objects.filter(Amenity="Wheelchair")
    Wheelchairs = WheelchairBuses.union(WheelchairTrains)

    ToiletBuses = BusStopAmenity.objects.filter(Amenity="Toilet")
    ToiletTrains = TrainStationAmenity.objects.filter(Amenity="Toilet")
    Toilets = ToiletBuses.union(ToiletTrains)

    Exits = TrainStationExit.objects.all()
    Buses = BusStop.objects.all()
    TrainStations = TrainStation.objects.all().order_by('Longitude')

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    day = datetime.date.today().strftime("%A")
    time = timezone.localtime().time()

    public_holidays = ""
    timing_data=None

    with open("LearnItGlobal/PublicHolidaysfor2026.csv", "r") as file:
        public_holidays = file.read()

    with open("LearnItGlobal/timings.json", "r") as file:
        timing_data = json.load(file)

    display_times_NEL = []

    if day == "Saturday":
        times = [datetime.datetime.strptime(item, "%H:%M").time() for item in timing_data["timetable"]["saturdays"]]
    elif day == "Sunday" or date in public_holidays:
        times = [datetime.datetime.strptime(item, "%H:%M").time() for item in timing_data["timetable"]["sundays_public_holidays"]]
    else:
        times = [datetime.datetime.strptime(item, "%H:%M").time() for item in timing_data["timetable"]["weekdays_mon_fri"]]

    first_service = datetime.datetime.strptime(str(times[0])[:5], "%H:%M").time()
    last_service = datetime.datetime.strptime(str(times[-1])[:5], "%H:%M").time()

    for time_train in times:
        if time_train>time:
            display_times_NEL.append(time_train)


    url = "https://datamall2.mytransport.sg/ltaodataservice/TrainServiceAlerts"
    headers = {
        "AccountKey": "DYcp2xF6QNKde4zceePCkw==",
        "accept": "application/json"
    }
    cached = cache.get("train_alerts")



    if cached:
        value = cached["value"]

    else:
        response = requests.get(url, headers=headers)
        jsontext = json.loads(response.text)
        value = jsontext["value"]

        cache.set("train_alerts", jsontext, timeout=60)

    messages = value["Message"]


    if not display_times_NEL:
        average_time = "No more trains today."

    else:
        tz = ZoneInfo("Asia/Singapore")
        time_now = timezone.localtime(timezone.now()).time()

        now = datetime.datetime.combine(datetime.date.today(), time_now)
        first = datetime.datetime.combine(datetime.date.today(), first_service)
        last = datetime.datetime.combine(datetime.date.today(), last_service)

        if now > first and now < last:
            average_time = (datetime.datetime.combine(datetime.date.today(),display_times_NEL[3]) - datetime.datetime.combine(datetime.date.today(), display_times_NEL[2]))
            average_time = str(average_time)[3]
            average_time = f"Every {average_time} min"

        else:
            average_time = "No trains now."

        print(first)
        first_service = str(first)[11:16]
        last_service = str(last)[11:16]

    Coordinates["Alerts"] = [message["Content"][:300] + "..." for message in messages]
    Coordinates["ATM"] = [[ATM.Latitude, ATM.Longitude, ATM.AmenityName, ATM.AmenityLocationDescription, ATM.Amenity] for ATM in ATMs]
    Coordinates["Convenience"] = [[Convenience.Latitude, Convenience.Longitude, Convenience.AmenityName, Convenience.AmenityLocationDescription, Convenience.Amenity] for Convenience in Conveniences]
    Coordinates["Wheelchair"] = [[Wheelchair.Latitude, Wheelchair.Longitude, Wheelchair.AmenityName, Wheelchair.AmenityLocationDescription, Wheelchair.Amenity] for Wheelchair in Wheelchairs]
    Coordinates["Toilet"] = [[Toilet.Latitude, Toilet.Longitude, Toilet.AmenityName, Toilet.AmenityLocationDescription, Toilet.Amenity] for Toilet in Toilets]
    Coordinates["BusStop"] = []
    Coordinates["TrainStation"] = []
    Coordinates["TrainStationExit"] = [[Exit.ExitDigit, Exit.ExitDescription, Exit.Latitude, Exit.Longitude] for Exit in Exits]
    Coordinates["FirstTrain"] = first_service
    Coordinates["LastTrain"] = last_service


    for bus in Buses:
        amenities = (
            BusStopAmenity.objects
            .filter(BusStopCode=bus.BusStopCode)
            .values_list("Amenity", "AmenityLocationDescription")
            .order_by('Amenity')
        )
        amenities_format = [[row[0], row[1]] for row in amenities]
        Coordinates["BusStop"].append([
            bus.Latitude,
            bus.Longitude,
            bus.BusStopName,
            bus.BusStopCode,
            amenities_format,
        ])

    for trainstation in TrainStations:
        lines = (
            TrainDetail.objects
            .filter(TrainStationCode=trainstation.TrainStationCode)
            .values_list("Line", flat=True)
            .distinct()
        )
        amenities = (
            TrainStationAmenity.objects
            .filter(TrainStationCode=trainstation.TrainStationCode)
            .values_list("Amenity", "AmenityLocationDescription")
            .order_by('Amenity')
        )
        exits = (
            TrainStationExit.objects
            .filter(TrainStationCode=trainstation.TrainStationCode)
            .values_list("ExitDigit", "ExitDescription")
            .order_by("ExitDigit")
        )

        amenities_format = [[row[0], row[1]] for row in list(amenities)]

        data_crowding = requests.get(url="https://datamall2.mytransport.sg/ltaodataservice/PCDRealTime",
                                     headers={"AccountKey": "DYcp2xF6QNKde4zceePCkw==",
                                              "accept": "account/key"},
                                     params={'TrainLine': "NEL"}
                                     ).json()

        level = ''
        try:
            for station in data_crowding['value']:
                if station["Station"] == trainstation.LineCode:
                    level = station['CrowdLevel']

        except:
            level = 'X'


        Coordinates["TrainStation"].append([
            trainstation.Latitude,
            trainstation.Longitude,
            trainstation.TrainStationName,
            list(lines),
            amenities_format,
            average_time,
            level,
            trainstation.LineCode,
            list(exits)
        ])


    if action:
        #direction north = True
        # want to get the data about the locations of each of the things in the form
        # {
        # 'ATM': [[coord1, coord2], [coord3, coord4],....]
        #
        # }
        # direction south = False in database
        if action == 'explore':
            return render(request, 'main.html', context={'Action': 'explore',
                                                                       'Amenities': Coordinates,
                                                                        'TrainTimings': times})

        elif action == 'directions':
            return render(request, 'main.html', context={'Action': 'directions',
                                                                      'Amenities': Coordinates,
                                                                      'TrainTimings': times})

        else:
            return HttpResponse("Not Found")

    else:
        return render(request, context={'Action': 'directions',
                                'Amenities': 'Coordinates'})


def get_bus_stops(request):
    code = request.GET.get("code").strip("/")
    cached = cache.get(f"bus_arrival_{code}")
    response = ""

    if not cached:
        url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"
        headers = {
            "AccountKey": "DYcp2xF6QNKde4zceePCkw==",
            "accept": "application/json"
        }

        response = requests.get(url, headers=headers, params={"BusStopCode": code})
        response = response.json()
        cache.set(f"bus_arrival_{code}", json.dumps(response))

    else:
        response = json.loads(cached)

    return JsonResponse(response, safe=False)


def get_bus_routes(request):
    cached = cache.get("bus_routes")
    response = []
    skip = 0

    if not cached:
        headers = {
            "AccountKey": "DYcp2xF6QNKde4zceePCkw==",
            "accept": "application/json"
        }

        while True:
            url = f"https://datamall2.mytransport.sg/ltaodataservice/BusRoutes?$skip={skip}"
            api_result = requests.get(url, headers=headers)

            result = json.loads(api_result.text)

            if result['value'] == []:
                break

            response.extend(result['value'])
            skip+=500


    else:
        response = cached

    cache.set("bus_routes", response)

    final_dict = {}
    final_dict['value'] = response

    return JsonResponse(final_dict, safe=False)

def get_bus_stations(request):
    cached = cache.get("bus_stations")
    response = []
    skip = 0

    if not cached:
        headers = {
            "AccountKey": "DYcp2xF6QNKde4zceePCkw==",
            "accept": "application/json"
        }

        while True:
            url = f"https://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={skip}"
            api_result = requests.get(url, headers=headers)
            result = json.loads(api_result.text)

            if result['value'] == []:
                break

            response.extend(result['value'])
            skip+=500

    else:
        response = cached

    with open("bus_stations.txt", "w") as f:
        f.write(json.dumps(response))

    cache.set("bus_stations", response)

    final_dict = {}
    final_dict['value'] = response

    return JsonResponse(final_dict, safe=False)

