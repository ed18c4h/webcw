from django.db import models

# Create your models here.
# todo/todo_api/models.py

from django.contrib.auth.models import User


    
class Flights(models.Model):
    number = models.IntegerField(max_length = 10)
    origin = models.CharField(max_length= 50)
    destination = models.CharField(max_length= 50)
    scheduledAt = models.DateTimeField(null=True, blank=True)
    maxSeatCapacity = models.IntegerField(max_length = 5)
    currentSeatCapacity = models.IntegerField(max_length = 5)

class Passengers(models.Model):
    userName = models.CharField(max_length= 50)
    
class PaymentProviders(models.Model):
    companyName = models.CharField(max_length= 50)
    
class SeatBookings(models.Model):
    passengerId = models.ForeignKey(Passengers, on_delete = models.CASCADE, blank = True, null = True)
    flightId = models.ForeignKey(Flights, on_delete = models.CASCADE, blank = True, null = True)
    seatNumber = models.IntegerField(max_length =5)
    
    
class Transactions(models.Model):
    paymentId =  models.ForeignKey(PaymentProviders, on_delete = models.CASCADE, blank = True, null = True)
    seatBookingId =  models.ForeignKey(SeatBookings, on_delete = models.CASCADE, blank = True, null = True)
