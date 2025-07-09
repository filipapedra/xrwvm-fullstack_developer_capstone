from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views 

app_name = 'djangoapp'

urlpatterns = [
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='registration', view=views.registration_request, name='registration'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path('dealerships/<str:state>/', views.get_dealerships, name='get_dealerships'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='get_dealer_details'),
    path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),
    path(route='add_review', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
