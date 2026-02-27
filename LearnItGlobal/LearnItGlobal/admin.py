from django.contrib import admin
from .models import *

admin.site.register(BusStop)
admin.site.register(BusDetail)
admin.site.register(BusStopAmenity)

admin.site.register(TrainStation)
admin.site.register(TrainStationExit)
admin.site.register(TrainStationAmenity)
admin.site.register(TrainDetail)

