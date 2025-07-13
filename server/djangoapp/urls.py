from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views 

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration_request, name='registration'),
    path('get_cars', views.get_cars, name='getcars'),
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealerships/', views.get_dealerships, name='get_dealerships'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='get_dealer_details'),
    path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('add_review/<int:dealer_id>', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
