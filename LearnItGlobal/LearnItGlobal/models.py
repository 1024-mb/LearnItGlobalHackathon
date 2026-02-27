
from django.db import models

class BusStop(models.Model):
    BusStopCode = models.IntegerField(primary_key=True)
    BusStopName = models.CharField(max_length=200)
    Latitude = models.DecimalField(max_digits=20, decimal_places=10)
    Longitude = models.DecimalField(max_digits=20, decimal_places=10)

class BusDetail(models.Model):
    BusDetailCode = models.BigAutoField(primary_key=True)
    BusNumber = models.IntegerField()
    BusStopCode = models.ForeignKey(BusStop, on_delete=models.CASCADE, db_column='BusStopCode')

class BusStopAmenity(models.Model):
    BusStopAmenityCode = models.BigAutoField(primary_key=True)
    BusStopCode = models.ForeignKey(BusStop, on_delete=models.CASCADE, db_column='BusStopCode')

    class AmenityChoices(models.TextChoices):
        CONVENIENCE_STORE = "Convenience Store"
        WHEELCHAIR = "Wheelchair"
        TOILET = "Toilet"
        ATM = "ATM"

    Amenity = models.CharField(max_length=50, choices=AmenityChoices)
    AmenityName = models.CharField(max_length=200)
    Latitude = models.DecimalField(max_digits=20, decimal_places=10)
    Longitude = models.DecimalField(max_digits=20, decimal_places=10)
    AmenityLocationDescription = models.CharField(max_length=100, default='No Further Information')

class TrainStation(models.Model):
    TrainStationCode = models.BigAutoField(primary_key=True)

    Latitude = models.DecimalField(max_digits=20, decimal_places=10)
    Longitude = models.DecimalField(max_digits=20, decimal_places=10)

    TrainStationName = models.CharField(max_length=200)
    LineCode = models.CharField(max_length=10)

class TrainStationAmenity(models.Model):
    TrainStationAmenityCode = models.BigAutoField(primary_key=True)
    TrainStationCode = models.ForeignKey(TrainStation, on_delete=models.CASCADE)

    class AmenityChoices(models.TextChoices):
        CONVENIENCE_STORE = "Convenience Store"
        WHEELCHAIR = "Wheelchair"
        TOILET = "Toilet"
        ATM = "ATM"

    Amenity = models.CharField(max_length=50, choices=AmenityChoices)
    AmenityName = models.CharField(max_length=200)
    Latitude = models.DecimalField(max_digits=20, decimal_places=10)
    Longitude = models.DecimalField(max_digits=20, decimal_places=10)
    AmenityLocationDescription = models.CharField(max_length=100, default='No Further Information')


class TrainStationExit(models.Model):
    TrainStationExitCode = models.BigAutoField(primary_key=True)
    TrainStationCode = models.ForeignKey(TrainStation, on_delete=models.CASCADE)
    Latitude = models.DecimalField(max_digits=20, decimal_places=10)
    Longitude = models.DecimalField(max_digits=20, decimal_places=10)
    ExitDescription = models.CharField(max_length=200)
    ExitDigit = models.CharField(max_length=1)

class TrainDetail(models.Model):
    TrainDetailCode = models.BigAutoField(primary_key=True)
    TrainStationCode = models.ForeignKey(TrainStation, on_delete=models.CASCADE)
    TrainStationLineNumber = models.IntegerField()

    class Line(models.TextChoices):
        EW = "East-West"
        NS = "North-South"
        NE = "North-East"
        CCL = "Circle"
        TEL = "Thompson-East Coast"
        BPLRT = "Bukit Panjang LRT"
        DT = "Downtown"
        SKLRT = "Sengkang LRT"
        PGLRT = "Punggol LRT"

    Line = models.CharField(max_length=50, choices=Line)

