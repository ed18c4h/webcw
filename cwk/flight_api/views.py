from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import  Flights,Passengers,SeatBookings,PaymentProviders,Transactions

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q

class FlightApiBook(APIView):
    def post(self, request,format=None):
        if request.method == 'POST':
            data = json.loads(request.body)

            # Extract information from the JSON data
            passenger_name = data.get('passengerName')
            flight_number = data.get('flightNumber')
            scheduled_at = data.get('scheduledAt')
            payment_info = data.get('payment')

            # Check if the flight is available and has not reached the max seat capacity
            try:
                flight = Flights.objects.get(number=flight_number)
                if flight.currentSeatCapacity >= flight.maxSeatCapacity:
                    return JsonResponse({'message': 'The flight has reached maximum seat capacity.'}, status=400)
            except Flights.DoesNotExist:
                return JsonResponse({'message': 'The specified flight does not exist.'}, status=400)

            # Create the seat booking
            passenger = Passengers.objects.create(userName=passenger_name)
            seat_booking = SeatBookings.objects.create(passengerId=passenger, flightId=flight)
            
            # Process payment information
            card_number = payment_info.get('cardNumber')
            expiry = payment_info.get('expiry')
            cvv = payment_info.get('cvv')
            email = payment_info.get('email')
            password = payment_info.get('password')
            
            # Save payment and transaction details
            payment_provider = PaymentProviders.objects.create(companyName='Your Payment Provider')
            transaction = Transactions.objects.create(paymentId=payment_provider, seatBookingId=seat_booking)
            
            return JsonResponse({'message': 'Seat booking successful.'}, status=200)

        #return Response({'message': 'Invalid request method.'}, status=405)
        return HttpResponse(status=204)

class FlightApiSearch(APIView):

    # 1. List all
    def get(self, request, origin_code, destination_code, date):
        
 
        try:
            # Convert the provided date string to a datetime object
            search_date = datetime.strptime(date, '%d-%m-%Y').date()

            # Retrieve the flights with the matching criteria
            flights = Flights.objects.filter(
                Q(origin=origin_code) & Q(destination=destination_code) & Q(scheduledAt__date=search_date)
            )

            # Create a list to store flight information
            flight_data = []
            for flight in flights:
                flight_data.append({
                    'number': flight.number,
                    'origin': flight.origin,
                    'destination': flight.destination,
                    'scheduledAt': flight.scheduledAt.strftime('%d-%m-%Y %H:%M'),
                    'maxSeatCapacity': flight.maxSeatCapacity,
                    'currentSeatCapacity': flight.currentSeatCapacity,
                })

            return JsonResponse({'flights': flight_data}, status=200)
        
        except ValueError:
            return JsonResponse({'message': 'Invalid date format. Please provide date in DD-MM-YYYY format.'}, status=400)

  
class FlightApiDelete(APIView):
    
    
       def delete(self, request, booking_num):
        
        if request.method == 'DELETE':
           # data = json.loads(request.body)
            booking_reference = booking_num

            try:
                seat_booking = SeatBookings.objects.get(id=booking_reference)
                seat_booking.delete()
                return JsonResponse({'status': 'deleted'}, status=200)
            except SeatBookings.DoesNotExist:
                return JsonResponse({'status': 'error'}, status=404)

        return JsonResponse({'message': 'Invalid request method.'}, status=405)