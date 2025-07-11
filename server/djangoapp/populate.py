from .models import CarMake, CarModel, Dealer

def initiate():
    # Create dummy dealers
    dealer1, _ = Dealer.objects.get_or_create(
        name="Default Dealer 1",
        defaults={
            "address": "123 Main St",
            "city": "Sample City",
            "state": "CA",
            "zip_code": "90210"
        }
    )
    dealer2, _ = Dealer.objects.get_or_create(
        name="Default Dealer 2",
        defaults={
            "address": "456 Elm St",
            "city": "Other City",
            "state": "NY",
            "zip_code": "10001"
        }
    )

    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]
    car_make_instances = [CarMake.objects.create(**data) for data in car_make_data]

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer": dealer1},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer": dealer1},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer": dealer1},
        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer": dealer2},
        {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer": dealer2},
        {"name": "E-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer": dealer2},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            type=data['type'],
            year=data['year'],
            car_make=data['car_make'],
            dealer=data['dealer']  
        )