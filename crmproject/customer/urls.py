from django.urls import path
from .views import CustomerAPIView,RegisterAPI,LoginAPI,RepresentativesAPIView,VendorsInsightsAPIView,VendorsMailSentAPIView

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view(), name='login'),
    path('customer', CustomerAPIView.as_view(), name='customer'),
    path('represent',RepresentativesAPIView.as_view(),name = 'represent'),
    path('insight',VendorsInsightsAPIView.as_view(),name = 'insight'),
    path('mailsentinfo',VendorsMailSentAPIView.as_view(),name = 'mailsentinfo')
]
