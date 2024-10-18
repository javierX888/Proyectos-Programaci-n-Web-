from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('propertiesdata/', views.getJsonPropertyData, name='propertiesdata'),
    path('yourpropertiesdata/', views.getJsonYourPropertyData, name='yourpropertiesdata'),
    path('property/<int:property_id>/', views.property, name='property'),
    path('propertyPhotosPath/<int:property_id>/', views.getJsonPropertyPhotosPath, name='propertyPhotosPath'),
    path('propertyPriceRange/<int:property_id>/', views.getJsonPropertyPriceRange, name='propertyPriceRange'),
    path('yourproperties/', views.yourproperties, name='yourproperties'),
    path('reservation/<int:property_id>/<int:room_no>/<str:check_in>/<str:check_out>/<int:guests>',
        views.reservation, name='reservation'),
    path('availableRooms/<int:property_id>/<str:check_in>/<str:check_out>/<int:guests>',
        views.getJsonAvailableRoomsData, name='availableRooms'),
    path('myRents/', views.myRents, name='myRents'),
    path('myGuests/', views.myGuests, name='myGuests'),
    path('updateReview/<int:rent_id>/<str:owner_rating>/<str:property_rating>/<str:owner_review>/<str:property_review>', views.updateReview, name='updateReview')
]