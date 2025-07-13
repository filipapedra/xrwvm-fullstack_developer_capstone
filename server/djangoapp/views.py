from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments
import os
import requests


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    response = {"userName": username}
    if user is not None:
        login(request, user)
        response["status"] = "Authenticated"
    else:
        response["status"] = "Authentication Failed"
    return JsonResponse(response)


@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration_request(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name,
        password=password, email=email
    )
    login(request, user)

def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make').all()
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = f"http://localhost:3030/fetchDealers/"
    else:
        endpoint = f"http://localhost:3030/fetchDealers/"+state
    dealerships = requests.get(endpoint).json()
    # print(dealerships)  # DEBUG: See what backend returns
    return JsonResponse({"status":200,"dealers":dealerships})


def get_dealer_details(request, dealer_id):
    
    print(f"id = {dealer_id}")
    if dealer_id:
        endpoint = "http://localhost:3030/fetchDealer/" + str(dealer_id)
        dealership = requests.get(endpoint).json()
        print(dealership)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "http://localhost:3030/fetchReviews/dealer/" + str(dealer_id)
        reviews =  requests.get(endpoint).json()
        # If reviews is None or empty list, handle gracefully
        if reviews is None:
            reviews = []
        for review_detail in reviews:
            # Assume each review_detail has a 'review' key containing the review text
            response = analyze_review_sentiments(review_detail.get('review', ''))
            print(response)  # For debugging, remove in production
            review_detail['sentiment'] = response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def add_review(request, dealer_id):


 
    if(request.user.is_anonymous == False):
        if request.method == 'POST':
            data = json.loads(request.body)
            review_data = {
                "name": data.get('name'),
                "dealership": dealer_id,
                "review": data.get('review'),
                "purchase": data.get('purchase', False),
                "purchase_date": data.get('purchase_date'),
                "car_make": data.get('car_make'),
                "car_model": data.get('car_model'),
                "car_year": data.get('car_year')
            }
            print(review_data)
            try:
                response = requests.post(
                    'http://localhost:3030/insert_review',  # or full production URL
                    json=review_data,
                    headers={'Content-Type': 'application/json'}
                )

                return JsonResponse(response.json(), status=response.status_code)
            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': 'Failed to connect to review service', 'details': str(e)}, status=500)
       
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})